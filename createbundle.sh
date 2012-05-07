#!/bin/bash
echo "Creating bundle/ajedrez.xo"
rm -rdf bundle
mkdir bundle
mkdir bundle/Ajedrez.activity
cp *.py bundle/Ajedrez.activity/
cp -R sugargame bundle/Ajedrez.activity/
cp -r po bundle/Ajedrez.activity/

mkdir bundle/Ajedrez.activity/engines
cp engines/gnuchess-linux bundle/Ajedrez.activity/engines/

#mkdir bundle/Ajedrez.activity/data
#cp -R data/* bundle/Ajedrez.activity/data/

mkdir bundle/Ajedrez.activity/data_bw
cp -R data_bw/* bundle/Ajedrez.activity/data_bw/

mkdir bundle/Ajedrez.activity/activity
cp activity-icon.svg bundle/Ajedrez.activity/activity/
cd bundle

#Create activity.info
cat > Ajedrez.activity/activity/activity.info <<EOF

[Activity]
name = Ajedrez
service_name = org.x.ajedrezactivity
activity_version = 1
host_version = 1
bundle_id = org.x.ajedrezactivity
icon = activity-icon
class = chessactivity.ChessActivity
show_launcher = yes
EOF

#Create setup.py
cat > Ajedrez.activity/setup.py <<EOF
from sugar.activity import bundlebuilder
if __name__ == "__main__":
    bundlebuilder.start("ajedrezactivity")
EOF

find Ajedrez.activity -type f | grep -v MANIFEST | grep -v ".svn" | sed -e 's,^Ajedrez.activity/,,' > Ajedrez.activity/MANIFEST
rm -f ajedrez.xo
zip -rq ajedrez.xo Ajedrez.activity
#zip -dq ajedrez.xo "*.svn*"
cd ..
