import cv2
import numpy as np
import mediapipe as mp

def initialize_game():
    # Initialize the webcam
    cap = cv2.VideoCapture(0)

    # Check if the webcam opened successfully
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        exit()

    # Set the initial positions and properties of the paddle and ball
    paddle_width = 100
    paddle_height = 20
    paddle_x = 200
    paddle_y = 450
    paddle_speed = 10

    ball_x = 100
    ball_y = 100
    ball_radius = 20
    ball_speed_x = 10  # Increase the horizontal speed
    ball_speed_y = 10  # Increase the vertical speed

    score = 0
    game_over = False

    return cap, paddle_width, paddle_height, paddle_x, paddle_y, paddle_speed, \
        ball_x, ball_y, ball_radius, ball_speed_x, ball_speed_y, score, game_over

def main():
    cap, paddle_width, paddle_height, paddle_x, paddle_y, paddle_speed, \
        ball_x, ball_y, ball_radius, ball_speed_x, ball_speed_y, score, game_over = initialize_game()

    # Initialize the MediaPipe Hands model for hand tracking
    mp_hands = mp.solutions.hands.Hands()

    # Get the screen width and height
    screen_width = int(cap.get(3))
    screen_height = int(cap.get(4))

    # Create a fullscreen window
    cv2.namedWindow("OpenSource PingPong", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("OpenSource PingPong", cv2.WND_PROP_FULLSCREEN, cv2.WND_PROP_FULLSCREEN)

    while True:
        ret, frame = cap.read()

        # Check if frame capture was successful
        if not ret:
            print("Error: Could not read a frame from the webcam.")
            break

        if not game_over:
            # Perform hand detection and tracking
            frame = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)
            results = mp_hands.process(frame)

            # Extract the x-coordinate of the hand's center, you may need to adjust this based on your hand tracking model
            if results.multi_hand_landmarks:
                hand_landmarks = results.multi_hand_landmarks[0]
                hand_center_x = int(hand_landmarks.landmark[mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP].x * screen_width)
                paddle_x = hand_center_x - paddle_width // 2

            # Draw the player's paddle
            cv2.rectangle(frame, (paddle_x, paddle_y), (paddle_x + paddle_width, paddle_y + paddle_height), (0, 0, 255), -1)

            # Draw the ball
            cv2.circle(frame, (ball_x, ball_y), ball_radius, (0, 255, 0), -1)

            # Move the ball
            ball_x += ball_speed_x
            ball_y += ball_speed_y

            # Ball collision with walls
            if ball_x + ball_radius > screen_width or ball_x - ball_radius < 0:
                ball_speed_x = -ball_speed_x
            if ball_y - ball_radius < 0:
                ball_speed_y = -ball_speed_y

            # Ball collision with paddle
            if paddle_x < ball_x < paddle_x + paddle_width and paddle_y < ball_y + paddle_height:
                ball_speed_y = -ball_speed_y
                score += 10
                ball_speed_x += 20  # Increase ball speed when the player scores

            # Check for game over condition
            if ball_y + ball_radius > screen_height:
                game_over = True

            # Show the score
            cv2.putText(frame, f"Score: {score}", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        else:
            # Display a game over message
            cv2.putText(frame, "Press 'R' to Try Again.", (screen_width // 4, screen_height // 2), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            # Check for 'R' key to reset the game
            key = cv2.waitKey(1)
            if key == 114:  # 'R' key to reset
                cap.release()
                cv2.destroyAllWindows()
                cap, paddle_width, paddle_height, paddle_x, paddle_y, paddle_speed, \
                    ball_x, ball_y, ball_radius, ball_speed_x, ball_speed_y, score, game_over = initialize_game()

        # Show the frame
        cv2.imshow("OpenSource PingPong", frame)

        # Get user input for paddle movement
        key = cv2.waitKey(1)
        if key == 27:  # ESC key to exit
            break

    # Release the webcam and close the window
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
