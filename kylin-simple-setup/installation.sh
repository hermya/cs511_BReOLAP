sudo ls -lart
sudo docker pull apachekylin/apache-kylin-standalone:kylin-4.0.1-mondrian
sudo docker run -d \
-m 8G \
-p 7070:7070 \
-p 7080:7080 \
-p 8088:8088 \
-p 50070:50070 \
-p 8032:8032 \
-p 8042:8042 \
-p 2181:2181 \
apachekylin/apache-kylin-standalone:kylin-4.0.1-mondrian
