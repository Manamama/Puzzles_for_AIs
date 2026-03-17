
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



Because: 


"There's a manifestUrl here with a ks= token that's probably expired. But the underlying endpoint might accept your browser session cookies instead of the token. Try: yt-dlp --referer ... --cookies-from-browser chrome {manifestUrl stripped of ks= and query params}"







