**Instructions**

1. Navigate to sample_api directory in the terminal and enter this command

    `docker-compose up --build --no-deps`
    
2. The terminal will display the status of the local server at: 127.0.0.1:5000

3. GET vehicle by ID

    Example: `GET: http://127.0.0.1:5000/vehicle/<vehicle_id>` 
    
4. POST a vehicle booking
    Application/json = {'vehicle_id': int, 'user_id': int}
 
    Example: `POST: http://127.0.0.1:5000/start_booking/`