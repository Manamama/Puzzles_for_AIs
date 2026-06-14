xmlstarlet ed -d '//@*[starts-with(name(),"font")]' \
              -d '//@style' \
              -d '//@fill' \
              -d '//@stroke' \
              -d '//@stroke-width' \
              -d '//@opacity' \
              -d '//@text-anchor' \
              -d '//@dominant-baseline' \
              -d '//@color' \
              /home/zezen/Downloads/GitHub/Puzzles_for_AIs/puzzles/programming/Strip/paper_fold_puzzle_2d_ai_friendly.svg > paper_fold_puzzle_2d_ai_friendly.svg_clean.svg
