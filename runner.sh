while true; do
  r=$(( $RANDOM % 10 )); 
  echo ==========================
  echo    r is $r
  echo ==========================
  if [ $r -eq 2 ] 
  then
	docker-compose exec mids ab -n 2 -c 1 -p project3/testdata/steel_sword_user_1.json -T 'application/json' http://localhost:5000/purchase_item/
  else
    if [ $r -eq 4 ]
    then
      docker-compose exec mids ab -n 3 -c 1 -p project3/testdata/steel_sword_user_1.json -T 'application/json' http://localhost:5000/sell_item/
    else
      if [ $r -eq 6 ]
      then
        docker-compose exec mids ab -n 1 -c 1 -p project3/testdata/steel_sword_user_2.json -T 'application/json' http://localhost:5000/purchase_item/ 
      else
        if [ $r -eq 8 ]
        then
          docker-compose exec mids ab -n 3 -c 1 -p project3/testdata/steel_sword_user_2.json -T 'application/json' http://localhost:5000/sell_item/
        fi
      fi
    fi
  fi
  sleep 2
done 
