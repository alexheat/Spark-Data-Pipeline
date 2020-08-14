while true; do
  user=$(( $RANDOM % 5 +1 )); 
  price=$(( $RANDOM % 29 +1 )); 
  sword=$(( $RANDOM % 2 )); 
  item="Steel Sword";
  item_type="Sword";
  
  if [ $sword -eq 1 ]
  then
    item="Steel Shield"
    item_type="Shield"
    
  fi
  
  payload="{\"user_id\":\"$user\", \"price\": $price, \"currency\": \"USD\", \"item\": \"$item\", \"item_type\": \"$item_type\"}"
  echo $payload > 'tmp.json'
  
  r=$(( $RANDOM % 2 )); 
  if [ $r -eq 1 ] 
  then
	 docker-compose exec mids ab -n 2 -c 1 -p project3/tmp.json -T 'application/json' http://localhost:5000/purchase_item/
  else
 	 docker-compose exec mids ab -n 2 -c 1 -p project3/tmp.json -T 'application/json' http://localhost:5000/sell_item/
  fi
  sleep 2
done 
