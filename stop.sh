ps -ef | grep 'Google Chrome Helper' | awk '{print $2}' | xargs kill -9
