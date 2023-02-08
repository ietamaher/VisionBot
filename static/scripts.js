        // Create JoyStick object into the DIV 'joy1Div'
        var Joy1 = new JoyStick('joy1Div');
        // Connect to the socket.io server
        var socket = io.connect('http://' + document.domain + ':' + location.port);
        socket.emit('my_event', {data: 'I\'m connected!'});

        socket.on('update_data', function(data) {
          var data_list = data.data;
          for (var i = 0; i < data_list.length; i++) {
            document.getElementById("data_value_" + i).innerHTML = data_list[i];
          }
        });

        // Handle button clicks
        function startMoveForward() {
            socket.emit('start_move_forward');
        }
         function stopMoveForward() {
            socket.emit('stop_move_forward');
        }
        const startCameraBtn = document.getElementById('start_camera_btn');
        const stopCameraBtn = document.getElementById('stop_camera_btn');

        startCameraBtn.addEventListener('click', function() {
            socket.emit('start_camera');
        });

        stopCameraBtn.addEventListener('click', function() {
            socket.emit('stop_camera');
        });
       document.getElementById('move_backward_button').onclick = function() {
            socket.emit('move_backward');
        };
        document.getElementById('move_left_button').onclick = function() {
            socket.emit('move_left');
        };
        document.getElementById('move_right_button').onclick = function() {
            socket.emit('move_right');
        };
        document.getElementById('speed_slider').onchange = function() {
            socket.emit('set_speed', this.value);
        };
        document.querySelectorAll("input[name='mode']").forEach(function(element) {
            element.addEventListener('change', function() {
                socket.emit('set_mode', this.value);
            });
        });

        document.querySelectorAll("input[name='jog']").forEach(function(element) {
            element.addEventListener('change', function() {
                socket.emit('set_jog', this.value);
            });
        });

        var joy1IinputPosX = document.getElementById("joy1PosizioneX");
        var joy1InputPosY = document.getElementById("joy1PosizioneY");
        var joy1Direzione = document.getElementById("joy1Direzione");
        var joy1X = document.getElementById("joy1X");
        var joy1Y = document.getElementById("joy1Y");

        setInterval(function(){
            var joy1IinputPosX=Joy1.GetPosX();
            if (joy1IinputPosX != 100) {
                socket.emit('my event', {data: joy1IinputPosX});
            }
        }, 100);
        setInterval(function(){ var joy1InputPosY=Joy1.GetPosY(); }, 50);
        setInterval(function(){ var joy1Direzione=Joy1.GetDir(); }, 50);
        setInterval(function(){ var joy1X=Joy1.GetX(); }, 50);
        setInterval(function(){ var joy1Y=Joy1.GetY(); }, 50);


        function readSettings() {
            fetch('/get_settings')
                .then(response => response.json())
                .then(data => fillForm(data))
        }

        function fillForm(data) {
            //console.log(data);
            document.getElementById("front_limit").value = data.frontLimitDistance;
            document.getElementById("rear_limit").value = data.rearLimitDistance;
        }

        function saveSettings() {
            // Get the form values
            const frontLimitDistance = document.getElementById('front_limit').value;
            const rearLimitDistance = document.getElementById('rear_limit').value;

            // Create a data object to send to the server
            const data = {
              frontLimitDistance: frontLimitDistance,
              rearLimitDistance: rearLimitDistance
            };
            console.log(data);
            // Use fetch to send the data to the server
            fetch('/save_settings', {
              method: 'POST',
              body: JSON.stringify(data),
              headers: {
                'Content-Type': 'application/json'
              }
            })
            .then(response => {
              if (response.ok) {
                console.log('Settings saved!');
              } else {
                console.log('Error saving settings');
              }
            })
            .catch(error => console.log(error));
        }

        var form=document.getElementById("formId");
        function submitForm(event){

           //Preventing page refresh
           event.preventDefault();
        }

        //Calling a function during form submission.
        form.addEventListener('submit', submitForm);

        window.onload = function() {
            readSettings();
        }

