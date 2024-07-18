#!/usr/bin/env python

import sys
import struct
import PIL
import PIL.Image
import os
import io


export_png = True
export_trim = False
export_full = False

os.environ["XBOX_IF"] = "none"
from xboxpy import nv2a

#FIXME: These are some magic numbers which are different for each file.
#       No idea how the game deals with this.
weirds = {
  "CS_ENV_1A_SMT.GZ": 0x10714,
  "CS_CS_1A_SMT.GZ": 0xD9814,
}

def xpr_extract(f):

  filename = os.path.basename(f.name)

  print("Opening '%s'" % (f.name))

  data = f.read()

  if filename in weirds:
    weird = weirds[filename]
  else:
    weird = 0

  #FIXME: This should be moved to or2.py
  if filename[0:4] == "SPR_":
    weird, unk4, unk8, xpr_offset = struct.unpack_from("<LLLL", data, 0)

    print("SPR_ unk4", unk4, hex(unk4))
    print("SPR_ unk8", unk8, hex(unk8))

    weird += 8
    xpr_offset += 8

  elif filename[0:4].upper() == "OBJ_":

    print(filename[-7:])
    #FIXME: Where to find this?
    #FIXME: Answer: See logic in cs__smt_extract.py
    xpr_offset = data.find(b'XPR0')
    assert(xpr_offset != -1)


    #FIXME: This seems to have a 16+28=44 byte header, judging by OBJ_SELECTOR_OBJ_SMT.GZ
    # Interesting to look at are also OBJ_MISSIONOBJ_SMT.GZ and OBJ_PC_COLOR_SMT.GZ
    print("%X" % xpr_offset)
    print("%X" % weird)
    unk0, unk4, weird, unkC = struct.unpack_from("<LLLL", data, 0)
    print("%X" % xpr_offset)
    print("%X" % weird)

    print("OBJ_ unk0", unk0, hex(unk0)) # maybe number of meshes?
    print("OBJ_ unk4", unk4, hex(unk4)) # number of textures?
    print("OBJ_ unkC", unkC, hex(unkC)) # data length?

    weird += 8
    xpr_offset += 8
    assert(weird + unkC == len(data))

  elif filename[0:3].upper() == "CS_":

    print(filename[-7:])
    #FIXME: Where to find this?
    xpr_offset = data.find(b'XPR0')

    if filename[-7:].upper() == "_SIN.GZ":
      print("CS_*_SIN has no XPR?")
      assert(xpr_offset == -1)
      return
    elif filename[-7:].upper() == "_BIN.GZ":
      print("CS_*_BIN has no XPR?")
      assert(xpr_offset == -1)
      return
    else:
      assert(xpr_offset != -1)

    print("%X" % xpr_offset)
    print("%X" % weird)
    unk0, unk4, weird, unkC = struct.unpack_from("<LLLL", data, 0)
    print("%X" % xpr_offset)
    print("%X" % weird)

    print("CS_ unk0", unk0, hex(unk0))
    print("CS_ unk4", unk4, hex(unk4))
    print("CS_ unkC", unkC, hex(unkC))

    weird += 0
    xpr_offset += 0

  else:
  
    weird, unk4, unk8, xpr_offset = struct.unpack_from("<LLLL", data, 0)

    print("SPR_ unk4", unk4, hex(unk4))
    print("SPR_ unk8", unk8, hex(unk8))

    weird += 0
    xpr_offset += -1

    #FIXME: We shouldn't have to search for this
    xpr_offset = data.find(b'XPR0')
    if xpr_offset == -1:
      print("No XPR?")
      return

    weird += xpr_offset + struct.unpack_from("<L", data, xpr_offset+8)[0]
    print("weird", weird, hex(weird))


  os.makedirs("./or2/%s/xpr/" % (filename), exist_ok=True)

  header = data[0:xpr_offset]
  open("./or2/%s/pre-xpr-header.bin" % (filename), 'wb').write(header)
  # Offset 28 seems to be length so that 32+length = len(data)?

  xpr = data[xpr_offset:]

  assert(xpr[0:4] == b'XPR0')
  assert(xpr[4:].find(b'XPR0') == -1)

  magic, size, header_size = struct.unpack_from("<LLL", xpr, 0)
  print(len(xpr))
  print(magic, size, header_size)
  print("Leftover: %d" % (len(xpr) - size))

  assert(size <= len(xpr))
  #assert(header_size % 0x800 == 0)


  open("./or2/%s/xpr-header.bin" % (filename), 'wb').write(xpr[0:header_size])


  print("\n  \"%s\": 0x%X,\n" % (filename, weird))



  open("./or2/%s/weird.bin" % (filename), 'wb').write(xpr[header_size:header_size+weird])

  fo = open("./or2/%s/xpr/xpr.mtl" % (filename), "wb")

  i = 0
  offset = 12
  while offset < header_size:

    flags = struct.unpack_from("<L", xpr, offset)[0]

    if flags == 0xFFFFFFFF:
      break

    flags_type = (flags >> 16) & 0x7
    flags_refs = flags & 0xFFFF
    flags_unk = (flags >> 19) & 0x1FFF

    if False:
      pass
    elif flags_type == 0x4:
      

      data_offset, unk1, fmt, unk2 = struct.unpack_from("<LLLL", xpr, offset+4)
      print(data_offset, unk1, fmt, unk2)
      #assert(unk0 == 0)
      assert(unk1 == 0)
      assert(unk2 == 0)
      #assert(unk3 == 0)

      #assert(end == 0xFFFFFFFF)

      fmt_cubemap = bool((fmt >> 2) & 1)
      fmt_type = (fmt >> 8) & 0xFF
      fmt_dimensions = (fmt >> 4) & 0xF
      fmt_levels = 1 << ((fmt >> 16) & 0xF)
      fmt_width = 1 << ((fmt >> 20) & 0xF)
      fmt_height = 1 << ((fmt >> 24) & 0xF)
      fmt_depth = 1 << ((fmt >> 28) & 0xF)

      real_data_offset = data_offset
      print("%d. Texture %d x %d x %d format 0x%X [offset 0x%X]" % (i, fmt_width, fmt_height, fmt_depth, fmt_type, data_offset))        

      #weird = 72; # most?
      pixel_data = data[data_offset+weird:]
      if export_full:
        open("./or2/%s/xpr/%d-texture-0-0-full.bin" % (filename, i), 'wb').write(pixel_data)

      if False:
        pass
      elif fmt_type == 0x6 or fmt_type == 0x7: # 0x6 = NV097_SET_TEXTURE_FORMAT_COLOR_SZ_A8R8G8B8
                                               # 0x7 = NV097_SET_TEXTURE_FORMAT_COLOR_SZ_X8R8G8B8

        pitch = fmt_width * 4

        pixel_data = pixel_data[0:pitch * fmt_height]
        pixel_data = nv2a.Unswizzle(pixel_data, 32, (fmt_width, fmt_height), pitch)

        im = PIL.Image.new("RGBA", (fmt_width, fmt_height))
        pixels = im.load()
        for y in range(0, fmt_height):
          for x in range(0, fmt_width):
            pixel_offset = (y * fmt_width + x) * 4
            r = pixel_data[pixel_offset+2]
            g = pixel_data[pixel_offset+1]
            b = pixel_data[pixel_offset+0]
            a = pixel_data[pixel_offset+3]
            pixels[x, y] = (r,g,b,a)
      elif fmt_type == 0x2: # 0x2 = NV097_SET_TEXTURE_FORMAT_COLOR_SZ_A1R5G5B5 0x02
        pitch = fmt_width * 2

        pixel_data = pixel_data[0:pitch * fmt_height]
        pixel_data = nv2a.Unswizzle(pixel_data, 16, (fmt_width, fmt_height), pitch)

        im = PIL.Image.new("RGBA", (fmt_width, fmt_height))
        pixels = im.load()
        for y in range(fmt_height):
          for x in range(fmt_width):
            pixel_offset = (y * fmt_width + x) * 2
            b = ((pixel_data[pixel_offset] & 0x1f) << 3)
            g = ((((pixel_data[pixel_offset] & 0xe0) >> 2) | ((pixel_data[pixel_offset+1] & 0x03) << 6))) + 8
            r = ((pixel_data[pixel_offset+1] & 0x7f) << 1)
            a = (((pixel_data[pixel_offset+1] & 0x80) >> 7) * 255)
            pixels[x, y] = (r,g,b,a)            
      elif fmt_type == 0x5: # 0x5 = NV097_SET_TEXTURE_FORMAT_COLOR_SZ_R5G6B5 0x05
                                        
        pitch = fmt_width * 2
        pixel_data = nv2a.Unswizzle(pixel_data, 16, (fmt_width, fmt_height), pitch)

        im = PIL.Image.new("RGBA", (fmt_width, fmt_height))
        pixels = im.load()
        for y in range(fmt_height):
          for x in range(fmt_width):
            pixel_offset = (y * fmt_width + x) * 2
            b = (pixel_data[pixel_offset] & 0x1f) << 3
            g = ((pixel_data[pixel_offset] & 0xe0) >> 3) | ((pixel_data[pixel_offset+1] & 0x07) << 5)
            r = pixel_data[pixel_offset+1] & 0xf8
            a = 255
            pixels[x, y] = (r,g,b,a)            

      elif fmt_type == 0xC: # NV097_SET_TEXTURE_FORMAT_COLOR_L_DXT1_A1R5G5B5
        pixel_data = pixel_data[0:fmt_width * fmt_height // 2]      
        im = PIL.Image.frombytes("RGBA", (fmt_width, fmt_height), pixel_data, 'bcn', 1)
      elif fmt_type == 0xE: # NV097_SET_TEXTURE_FORMAT_COLOR_L_DXT23_A8R8G8B8
        pixel_data = pixel_data[0:fmt_width * fmt_height]
        im = PIL.Image.frombytes("RGBA", (fmt_width, fmt_height), pixel_data, 'bcn', 2)
      elif fmt_type == 0xF: # NV097_SET_TEXTURE_FORMAT_COLOR_L_DXT45_A8R8G8B8
        pixel_data = pixel_data[0:fmt_width * fmt_height]
        im = PIL.Image.frombytes("RGBA", (fmt_width, fmt_height), pixel_data, 'bcn', 3)  
      else:
        print("Unknown texture format 0x%X" % fmt_type)
        assert(False)

      im = im.transpose(PIL.Image.FLIP_TOP_BOTTOM)
      if export_png:
        im.save("./or2/%s/xpr/%d-texture.png" % (filename, i))


      fo.write(b"newmtl texture-%d\n" % i)
      fo.write(b"map_Kd ../xpr/%d-texture.png\n" % (i))
      

      #FIXME: Export DDS instead?

      offset += 20
      start = real_data_offset+weird
      end = start + len(pixel_data)
      print("at ", start, "in XPR")
      print("data should be %d bytes until %d" % (len(pixel_data), end))

      if export_trim:
        open("./or2/%s/xpr/%d-texture-0-0-trim.bin" % (filename, i), 'wb').write(pixel_data)

    else:
      print("Unknown type 0x%X" % flags_type)
      assert(False)

    i += 1
  
  #FIXME: If this is not true, then we have to assert 0xFFFFFFFF as last type and padding
  #assert(offset == header_size)

  print(magic, size, header_size)



if __name__ == "__main__":
  for path in sys.argv[1:]:
    f = open(path, 'rb')
    xpr_extract(f)
