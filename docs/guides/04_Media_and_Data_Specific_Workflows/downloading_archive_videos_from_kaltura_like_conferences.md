
So the actual algorithm is:

Log into NVIDIA GTC, go to the session's page
Click "Debug Info" on the player
Copy the manifestUrl value — strip everything from ks/ onwards, keeping just up to a.m3u8, e.g.:
MANIFEST_URL=https://cdnapi-ev.kaltura.com/p/2935771/sp/293577100/playManifest/entryId/1_6jmbfa29/protocol/https/format/applehttp/flavorIds/.../a.m3u8

Run:

yt-dlp --referer "https://register.nvidia.com/" \
       --cookies-from-browser chrome \
       "MANIFEST_URL"

Done.




Or without cookies: 

`ffmpeg \
-headers "Referer: https://register.nvidia.com/" \
-i "https://cdnapi-ev.kaltura.com/p/2935771/sp/293577100/playManifest/entryId/1_p8p7en2p/protocol/https/format/applehttp/flavorIds/1_dt4uii77,1_rpsxbtfa,1_iuq6ikgv,1_vkdk6mct,1_0d6frfpn/ks/djJ8MjkzNTc3MXzAb8ENTdvlMc4tqnuYCm_mUqbCsaDKUEdZR1GIF6c7fUnUIe79LT-uHiI7xFYorkC6iwvHMIZvKZxpsnsZrKvBqqQMIN98YbHCfunWDw2fea7QRsZNGnFvFWazUrf5q3vUVtTKs2TLaGSpjhn7ORslmd2B94LzpeIzqkJL2kxm1J3wVqq6kwzz-vRVvpRYf9wcpkln9m2-Je31uY0xjZ2juaD6kBu1GtguWfhUVqs6Rs1g_1lFV0HfhZMJhtbPVGeB45VfSabp1TsawVKy4YTj0PvPsJ-qHBePKw3oGmzpFY3IS5K4_IeXeChXOFDqqXg=/a.m3u8?uiConfId=47254103&playSessionId=554e13b1-da68-c6a7-fdda-1efa818e491c:304f6db4-1a2e-8345-7884-03fbf4e8e4b0&referrer=aHR0cHM6Ly9yZWdpc3Rlci5udmlkaWEuY29tL2Zsb3cvbnZpZGlhL2d0YzI2L2FwL3BhZ2UvY2F0YWxvZ3Yvc2Vzc2lvbi8xNzY1MzczMjc3MTAxMDAxVHlhWg==&clientTag=html5:v3.17.75" \
-c copy -bsf:a aac_adtstoasc output.mp4` 




Because: 


"There's a manifestUrl here with a ks= token that's probably expired. But the underlying endpoint might accept your browser session cookies instead of the token. Try: yt-dlp --referer ... --cookies-from-browser chrome {manifestUrl stripped of ks= and query params}"







