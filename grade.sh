for i in `find . -name '*.zip'`; do
  cd ~/Documents/testing_cd_grade
  echo $i >> grade.csv
  unzip $i -d grade
  
  cd ~/Documents/testing_cd_grade/grade/
  cd ~/Documents/testing_cd_grade/grade/*/
  echo $PWD
  python ~/Documents/testing_cd_grade/position_check.py $PWD &
  #cd ~/Documents/testing_cd_grade/grade
  pwd
  #cmd =$PWD

  #cd ~/Documents/testing_cd_grade
  rosbag play *.bag 
  # sleep 1
  echo "removing"
  
  pwd
  echo "removing jdgfbdsjhfosdhfodshfodsoijdoigjdigoghg"

  rm -rf ~/Documents/testing_cd_grade/grade
  #cd ../
  pwd
  echo $i
  sleep 2
done

