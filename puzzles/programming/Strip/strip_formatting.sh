xmlstarlet ed -d '//@*[starts-with(name(),"font")]' \
              -d '//@style' \
              -d '//@fill' \
              -d '//@stroke' \
              -d '//@stroke-width' \
              -d '//@opacity' \
              -d '//@text-anchor' \
              -d '//@dominant-baseline' \
              -d '//@color' \
              paper_fold_puzzle_3d_svg.svg > clean.svg
