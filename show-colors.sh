#!/usr/bin/env bash

R=$'\033[0m'

echo "========================================"
echo "  CLAUDE-PRETTY CURRENT COLORS"
echo "========================================"
echo ""
echo -e "\033[31m[31] RED     - errors, tool_use_error${R}"
echo -e "\033[32m[32] GREEN   - Read tool, todo completed${R}"
echo -e "\033[33m[33] ORANGE  - Edit/Write tool, todo in_progress${R}"
echo -e "\033[34m[34] BLUE    - Task tool${R}"
echo -e "\033[35m[35] PURPLE  - Glob/Grep/Bash, other tools${R}"
echo -e "\033[36m[36] CYAN    - tool results${R}"
echo -e "\033[93m[93] YELLOW  - Todo header${R}"
echo -e "\033[2m[2]  DIM     - session info, done stats${R}"

echo ""
echo "========================================"
echo "  STANDARD COLORS (30-37)"
echo "========================================"
echo ""
for i in $(seq 30 37); do
  echo -e "\033[${i}m[${i}] The quick brown fox jumps over the lazy dog${R}"
done

echo ""
echo "========================================"
echo "  BRIGHT COLORS (90-97)"
echo "========================================"
echo ""
for i in $(seq 90 97); do
  echo -e "\033[${i}m[${i}] The quick brown fox jumps over the lazy dog${R}"
done

echo ""
echo "========================================"
echo "  BOLD + STANDARD (1;30-37)"
echo "========================================"
echo ""
for i in $(seq 30 37); do
  echo -e "\033[1;${i}m[1;${i}] The quick brown fox jumps over the lazy dog${R}"
done

echo ""
echo "========================================"
echo "  BOLD + BRIGHT (1;90-97)"
echo "========================================"
echo ""
for i in $(seq 90 97); do
  echo -e "\033[1;${i}m[1;${i}] The quick brown fox jumps over the lazy dog${R}"
done

echo ""
echo "========================================"
echo "  DIM + STANDARD (2;30-37)"
echo "========================================"
echo ""
for i in $(seq 30 37); do
  echo -e "\033[2;${i}m[2;${i}] The quick brown fox jumps over the lazy dog${R}"
done

echo ""
echo "========================================"
echo "  ITALIC (3;30-37)"
echo "========================================"
echo ""
for i in $(seq 30 37); do
  echo -e "\033[3;${i}m[3;${i}] The quick brown fox jumps over the lazy dog${R}"
done

echo ""
echo "========================================"
echo "  UNDERLINE + STANDARD (4;30-37)"
echo "========================================"
echo ""
for i in $(seq 30 37); do
  echo -e "\033[4;${i}m[4;${i}] The quick brown fox jumps over the lazy dog${R}"
done

echo ""
echo "========================================"
echo "  UNDERLINE + BRIGHT (4;90-97)"
echo "========================================"
echo ""
for i in $(seq 90 97); do
  echo -e "\033[4;${i}m[4;${i}] The quick brown fox jumps over the lazy dog${R}"
done

echo ""
echo "========================================"
echo "  BACKGROUND COLORS (40-47)"
echo "========================================"
echo ""
for i in $(seq 40 47); do
  echo -e "\033[${i}m[${i}] The quick brown fox jumps over the lazy dog${R}"
done

echo ""
echo "========================================"
echo "  BRIGHT BACKGROUND (100-107)"
echo "========================================"
echo ""
for i in $(seq 100 107); do
  echo -e "\033[${i}m[${i}] The quick brown fox jumps over the lazy dog${R}"
done

echo ""
echo "========================================"
echo "  FG + BG COMBOS"
echo "========================================"
echo ""
for fg in 30 31 32 33 34 35 36 37 90 91 92 93 94 95 96 97; do
  for bg in 40 41 42 43 44 45 46 47; do
    echo -ne "\033[${fg};${bg}m ${fg};${bg} ${R}"
  done
  echo ""
done

echo ""
echo "========================================"
echo "  256 COLORS (38;5;0-255)"
echo "========================================"
echo ""
for i in $(seq 0 15); do
  echo -ne "\033[38;5;${i}m[${i}] sample text  ${R}"
  if (( (i + 1) % 4 == 0 )); then echo ""; fi
done
echo ""
for i in $(seq 16 231); do
  echo -ne "\033[38;5;${i}m█${R}"
  if (( (i - 16 + 1) % 36 == 0 )); then echo ""; fi
done
echo ""
echo ""
for i in $(seq 232 255); do
  echo -ne "\033[38;5;${i}m█${R}"
done
echo ""

echo ""
echo "========================================"
echo "  MODIFIERS"
echo "========================================"
echo ""
echo -e "\033[0m[0] Normal / Reset${R}"
echo -e "\033[1m[1] Bold${R}"
echo -e "\033[2m[2] Dim${R}"
echo -e "\033[3m[3] Italic${R}"
echo -e "\033[4m[4] Underline${R}"
echo -e "\033[7m[7] Inverse${R}"
echo -e "\033[8m[8] Hidden${R}"
echo -e "\033[9m[9] Strikethrough${R}"

echo ""
echo "========================================"
echo "  USEFUL COMBOS FOR CLAUDE-PRETTY"
echo "========================================"
echo ""
echo -e "\033[1;32m[1;32] Bold Green${R}"
echo -e "\033[1;33m[1;33] Bold Orange/Yellow${R}"
echo -e "\033[1;34m[1;34] Bold Blue${R}"
echo -e "\033[1;35m[1;35] Bold Purple${R}"
echo -e "\033[1;36m[1;36] Bold Cyan${R}"
echo -e "\033[38;5;208m[38;5;208] 256-color Orange${R}"
echo -e "\033[38;5;214m[38;5;214] 256-color Gold${R}"
echo -e "\033[38;5;141m[38;5;141] 256-color Light Purple${R}"
echo -e "\033[38;5;75m[38;5;75] 256-color Light Blue${R}"
echo -e "\033[38;5;114m[38;5;114] 256-color Light Green${R}"
echo -e "\033[38;5;203m[38;5;203] 256-color Salmon${R}"
echo -e "\033[38;5;219m[38;5;219] 256-color Pink${R}"
echo -e "\033[38;5;117m[38;5;117] 256-color Sky Blue${R}"
echo -e "\033[38;5;156m[38;5;156] 256-color Mint${R}"
echo -e "\033[38;5;229m[38;5;229] 256-color Cream${R}"
