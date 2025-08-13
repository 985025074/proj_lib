cd /home/kokona/proj_lib/ctf_playground
echo "now pwd" $(pwd)
rm -rf ./challenge
scp -i /home/kokona/key -r hacker@pwn.college:/challenge .
echo "succeed" 