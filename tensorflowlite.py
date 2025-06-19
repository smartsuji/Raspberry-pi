import cv2
import numpy as np
import tflite_runtime.interpreter as tflite  # ✅ Use this for TensorFlow Lite


# ✅ Load TFLite Model
model_path = "/home/pi/model/converted_model.tflite"  # Make sure you have the .tflite model
interpreter = tflite.Interpreter(model_path=model_path)
interpreter.allocate_tensors()

# ✅ Get model input and output details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# ✅ Define class labels (Modify as per your dataset)
known_labels = ["Anjali", "Jenifer", "Sujithra", "Vignesh"]

# ✅ Load Haar Cascade for face detection
face_cascade = cv2.CascadeClassifier("/home/pi/haarcascades/haarcascade_frontalface_default.xml")

# ✅ Open webcam
cap = cv2.VideoCapture(0)  # Use 0 for the default camera

# ✅ Set video frame width and height
cap.set(3, 640)
cap.set(4, 480)

while True:
    success, frame = cap.read()
    if not success:
        print("Error: Could not access the camera.")
        break  

    # ✅ Convert frame to grayscale for better detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # ✅ Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50))

    for (x, y, w, h) in faces:
        # ✅ Extract the face ROI
        face_roi = frame[y:y + h, x:x + w]

        # ✅ Preprocess the face for model input
        img = cv2.resize(face_roi, (224, 224))  # Resize to match model input size
        img = np.expand_dims(img, axis=0)  # Add batch dimension
        img = img.astype(np.float32) / 255.0  # Normalize pixel values

        # ✅ Set the input tensor
        interpreter.set_tensor(input_details[0]['index'], img)

        # ✅ Run inference
        interpreter.invoke()

        # ✅ Get prediction results
        predictions = interpreter.get_tensor(output_details[0]['index'])
        class_index = np.argmax(predictions)  # Get the highest confidence class
        confidence = np.max(predictions) * 100  # Get confidence percentage

        # ✅ Identify the person
        if confidence >= 60:  # Confidence threshold (Adjust if needed)
            predicted_name = known_labels[class_index]
            text = f"{predicted_name} ({confidence:.2f}%)"
            color = (0, 255, 0)  # Green for known persons
        else:
            text = "Unknown - Access Denied"
            color = (0, 0, 255)  # Red for unknown persons

        # ✅ Draw bounding box around the face
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
        cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

    # ✅ Show the camera feed
    cv2.imshow("Live Face Recognition", frame)

    # ✅ Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break  

# ✅ Release the camera and close window
cap.release()
cv2.destroyAllWindows()
