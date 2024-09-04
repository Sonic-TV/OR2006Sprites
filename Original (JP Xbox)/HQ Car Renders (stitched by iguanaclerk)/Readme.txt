Missing, since they're C2C exclusive:  550 barchetta, superamerica, F430. spr_SPRANI_SUMO_VSLOAD_Exst probably has the highest quality for them.

https://github.com/emoose/OutRun2006Tweaks/issues/20#issuecomment-2285022883

I present, as a resource, the car selection renders from the Xbox port. They are cut up into different sprite pages in the texture files, so this will be easier to handle.
As these filled the screen in that version, they are higher quality than what's otherwise available (and all at a consistent level of quality). These are the 12 cars from the Xbox port (SP2 + two more) with all their available colors.

For any HD recreations these will be suitable for the arcade selection screen and with some outlining/dropshadow can be used for the Ghost icons. (Interestingly, the game uses the outlined/dropshadowed sprites for the SP2 Ghosts, but non-outlined/dropshadowed ones for the home port exclusive cars). The C2C online selection sprites have three more cars and the additional class skins, so those will be best sourced from the online loading sprite sheets in C2C.

These have a number of small fixes from the Xbox sprites:
F355 Spider: Dropshadow fixed
Dino 246GTS: Red highlight recolored to match the rest of the car for non-red colors.
Enzo Ferrari: Fixed the very rear of the car being red on other colors (they must have thought it was the taillight when recoloring, but it's part of the body).
Overlaid the available hi-res renders for the red Enzo, F50 and 250GTO to reduce compression artifacts. Manually did touch-up on the Dino 246GTS and a little on the Testarossa to accomplish the same thing.

The F50 has three alternate textures for black, white and yellow that have less artifacting on the hood because they are sized slightly differently and were hit less by compression. They are slightly smaller (they come from unused sprite sheets), so I've included them as alternates but they are probably otherwise preferable.
The F355 Spider has all 8 colors available in C2C, but I think some are unused in the Xbox port and the sprites for some color variants look unfinished. I've included all of them to be comprehensive.

Also included are the unused WIP textures for the Testarossa. These reflect the model originally being based off the official "Testarossa Spider" convertible (only one ever produced). Eventually, during production of the arcade game, they switched to making it look like the Testarossa convertible's appearance in Outrun 1 (which just carves the top off of a normal Testarossa).