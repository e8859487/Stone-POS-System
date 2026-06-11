---
name: deploy
description: Deploy code changes for the Stone-POS-System (福石園葡萄訂單管理系統) Flask app to PythonAnywhere. Use this whenever the user says "push", "部署", "deploy", "pull", "reload", or asks to publish/sync code changes to the live site at eechris1029.pythonanywhere.com.
---

# Deploy Stone-POS-System to PythonAnywhere

This project is deployed on PythonAnywhere (user: `eechris1029`). The live
site does NOT auto-deploy from GitHub — it runs whatever code is currently
checked out in `/home/eechris1029/mysite`, and the running process must be
reloaded for changes to take effect.

## Steps

1. **Push to GitHub** (from the user's local machine / this repo's working
   copy): commit the changes and run `git push origin master`
   (repo: https://github.com/e8859487/Stone-POS-System).

   - Claude cannot push from the sandbox (no GitHub credentials there).
     Ask the user to run `git push origin master` locally, or do it directly
     if Claude has a working git remote with credentials.

2. **Pull on PythonAnywhere** via the Claude in Chrome browser tools:
   - Open the bash console: https://www.pythonanywhere.com/user/eechris1029/consoles/21107540/
   - Click into the console, type `git pull`, and press Return immediately
     — no need to ask for confirmation first, this is a routine, safe command.
   - Confirm the output shows the new commit hash being fast-forwarded
     (not "Already up to date" — if it says that, the push in step 1 hasn't
     landed on GitHub yet).

3. **Reload the web app**:
   - Navigate to https://www.pythonanywhere.com/user/eechris1029/webapps/#tab_id_eechris1029_pythonanywhere_com
   - Find and click the green "Reload eechris1029.pythonanywhere.com" button.
   - A spinner appears next to the button while it reloads.

## Notes

- All three steps are part of one "deploy". If the user just says "push" or
  "deploy", do all applicable steps (push if needed, then pull, then reload)
  rather than stopping after step 1.
- If `git pull` on PythonAnywhere reports conflicts or errors, stop and show
  the user the output rather than trying to force-resolve it.
