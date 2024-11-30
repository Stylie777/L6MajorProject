# Setup git in actions
git config --global user.name "GitHub Action"
git config --global user.email "noreply@github.com"

# Update llvm
git submodule update --remote
git add llvm-project
git commit -m "[llvm-project] Update llvm-project version"
git push origin main