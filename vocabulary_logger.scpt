-- This script logs the selected word and the current date into a CSV file
set logFilePath to "/path/vocabulary.csv"

-- Get the clipboard content directly (ensure the text is copied manually before running the script)
set theWord to the clipboard as text
if theWord is not "" then
	set currentDate to (do shell script "date '+%Y-%m-%d %H:%M:%S'")
	set logEntry to "\"" & theWord & "\",\"" & currentDate & "\""
	do shell script "echo " & quoted form of logEntry & " >> " & logFilePath
	
	-- Display a confirmation message
	display notification "Logged: " & theWord & " at " & currentDate with title "Vocabulary Logger"
else
	-- Display an error message if the clipboard is empty
	display notification "No word copied to log." with title "Vocabulary Logger"
end if

