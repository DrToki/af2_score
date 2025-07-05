
DELETE old code 

Summarize progress in a PROGRESS.md file

NO interface{} or any{} - use concrete types!
NO time.Sleep() or busy waits - use channels for synchronization!
NO keeping old and new code together
NO migration functions or compatibility layers
NO versioned function names (processV2, handleNew)
NO custom error struct hierarchies
NO TODOs in final code

Meaningful names: userID not id

Stop - Don't spiral into complex solutions
Step back - Re-read the requirements --> look at plan.md
Simplify - The simple solution is usually correct
Ask - "I see two approaches: [A] vs [B]. Which do you prefer?"


