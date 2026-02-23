You are being tested to exercise all Claude Code internal tools. Do each step below in order:

1. Use Glob to list all files matching `*.sh` in the current directory
2. Use Read to read the file `show-colors.sh`
3. Use Write to create a file called `tmp-test-output.txt` with the content "hello from claude test"
4. Use Edit to change "hello from claude test" to "hello from claude test - updated" in `tmp-test-output.txt`
5. Use Grep to search for the word "color" in all `.sh` files
6. Use Bash to run `echo "bash tool works" && date`
7. Use the Task tool to launch a subagent with subagent_type "general-purpose" and the following prompt: "Do ALL of these steps in order: (a) Use Glob to find every file in the repo recursively with **/*. (b) Use Read to read ALL files you found - read them in parallel. (c) Use WebSearch to search for 'ANSI color codes terminal 2025 best practices'. (d) Use WebFetch to fetch https://en.wikipedia.org/wiki/ANSI_escape_code and extract the list of standard color codes. (e) Based on what you read from the repo files and the web research, use Write to create a file called 'subagent-report.md' with a detailed report that includes: a summary of what this repo does, a list of all ANSI colors currently used in claude-pretty.sh, a comparison with standard ANSI colors from your web research, and recommendations for additional colors that could improve readability. Make the report thorough."
8. Use the Task tool to launch a subagent with subagent_type "Bash" to run: "echo '--- bash subagent test ---' && uname -a && node --version && which claude && echo '--- done ---'"
9. Use TodoWrite to create a todo list with 3 items: "step one" (completed), "step two" (in_progress), "step three" (pending)
10. Print a final summary saying "All tools tested successfully"
