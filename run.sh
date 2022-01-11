echo "Pulling Repository"
git pull
echo "Auto Generating IOs"
python3 ./GenerateIOs.py
echo "Commit"
git add .
git commit -m "Auto Generation on `date +%Y%m%d`"
git push