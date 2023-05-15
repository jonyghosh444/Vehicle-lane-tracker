import cv2
import numpy as np
from object_detection import ObjectDetection
import math

# Initialize Object Detection
od = ObjectDetection()

cap = cv2.VideoCapture("vehicle1.mp4")

count = 0
center_points_prev_frame = []
prev_y = []

tracking_objects = {}
track_id = 0
tracking_objects_prev = {}

while True:
    if len(tracking_objects) == 0:
        ret, frame = cap.read()

        count += 1
        if not ret:
            break
        # 10 frame (skiping frame)
        # if count % 3 !=0:
        #     continue

        # Center points current frame
        center_points_crnt_frame = []
        crnt_y = []

        # Detect objects on frame
        (class_ids, scores, boxes) = od.detect(frame)
        boxno = 1
        for box in boxes:
            (x, y, w, h) = box
            cx = int((x + x + w)/2)
            cy = int((y+y+h)/2)
            print("Box No:", boxno, " ", x, y, w, h)

            # cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
            cv2.rectangle(frame, (x, y), (x + w, y+h), (0, 255, 0), 2)
            center_points_crnt_frame.append((cx, cy))
            boxno += 1

        if count <= 2:
            for pt in center_points_crnt_frame:
                for pt2 in center_points_prev_frame:
                    distance = math.hypot(pt2[0] - pt[0], pt2[1]-pt[1])

                    if distance < 20:
                        tracking_objects[track_id] = pt
                        track_id += 1
        else:

            tracking_objects_copy = tracking_objects.copy()
            center_points_crnt_frame_copy = center_points_crnt_frame.copy()

            for object_id, pt2 in tracking_objects_copy.items():
                object_exists = False
                for pt in center_points_crnt_frame_copy:
                    distance = math.hypot(pt2[0] - pt[0], pt2[1]-pt[1])

                    # update Ids position
                    if distance < 50:
                        tracking_objects[object_id] = pt
                        object_exists = True
                        if pt in center_points_crnt_frame:
                            center_points_crnt_frame.remove(pt)
                        continue
                # Remove Tds lost
                if not object_exists:
                    tracking_objects.pop(object_id)

            # Add new IDs found
            for pt in center_points_crnt_frame:
                tracking_objects[track_id] = pt
                track_id += 1
        for object_id, pt in tracking_objects.items():
            cv2.circle(frame, pt, 5, (0, 0, 255), -1)
            cv2.putText(frame, str(pt),
                        (pt[0], pt[1] - 7), 0, 1, (0, 0, 255), 2)
        print("Tracking objects")
        print(tracking_objects)

        print("Cur Frame Left points")
        print(center_points_crnt_frame)

        # area_1 = [(581,471),(389,665),(1118,658),(908,448)]
        # area_2 = [(990,437),(1201,555),(1371,446),(1195,401)]
        # lane = "Lane"
        # l = 1
        # for area in [area_1,area_2]:
        #     cv2.polylines(frame,[np.array(area, np.int32)], True,(15,220,10),6)
        #     text_position = tuple(np.mean(area, axis=0, dtype=int))  # Position the text at the centroid of the polyline
        #     cv2.putText(frame, lane+str(l), text_position, 0, 1, (0, 0, 255), 2,cv2.LINE_AA)
        #     l+=1
        print(f"Frame no: {count}")
        cv2.imshow("Frame", frame)
        # Make a copy of the points
        center_points_prev_frame = center_points_crnt_frame.copy()
        tracking_objects_prev = tracking_objects.copy()
        key = cv2.waitKey(33)
        if key == 27:
            break
    else:
        ret, frame = cap.read()

        count += 1
        if not ret:
            break
        # 10 frame (skiping frame)
        # if count % 3 !=0:
        #     continue

        # Center points current frame
        center_points_crnt_frame = []
        crnt_y = []

        # Detect objects on frame
        (class_ids, scores, boxes) = od.detect(frame)
        boxno = 1
        for box in boxes:
            (x, y, w, h) = box
            cx = int((x + x + w)/2)
            cy = int((y+y+h)/2)
            print("Box No:", boxno, " ", x, y, w, h)

            # cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
            cv2.rectangle(frame, (x, y), (x + w, y+h), (0, 255, 0), 2)
            center_points_crnt_frame.append((cx, cy))
            boxno += 1

        if count <= 2:
            for pt in center_points_crnt_frame:
                for pt2 in center_points_prev_frame:
                    distance = math.hypot(pt2[0] - pt[0], pt2[1]-pt[1])

                    if distance < 50:
                        tracking_objects[track_id] = pt
                        track_id += 1
        else:

            tracking_objects_copy = tracking_objects.copy()
            center_points_crnt_frame_copy = center_points_crnt_frame.copy()

            for object_id, pt2 in tracking_objects_copy.items():
                object_exists = False
                for pt in center_points_crnt_frame_copy:
                    distance = math.hypot(pt2[0] - pt[0], pt2[1]-pt[1])

                    # update Ids position
                    if distance < 20:
                        tracking_objects[object_id] = pt
                        object_exists = True
                        if pt in center_points_crnt_frame:
                            center_points_crnt_frame.remove(pt)
                        continue
                # Remove Tds lost
                if not object_exists:
                    tracking_objects.pop(object_id)

            # Add new IDs found
            for pt in center_points_crnt_frame:
                tracking_objects[track_id] = pt
                track_id += 1
        going = " is going by Lane 2"
        coming = " is coming by Lane 1"
        for object_id, pt in tracking_objects.items():
            for vidp, ptp in tracking_objects_prev.items():
                if object_id == vidp:
                    if pt[1]-ptp[1] < 0:
                        cv2.circle(frame, pt, 5, (0, 0, 255), -1)
                        cv2.putText(frame, str(object_id)+going,
                                    (pt[0], pt[1] - 7), 0, 1, (0, 0, 255), 2)
                    else:
                        cv2.circle(frame, pt, 5, (0, 0, 255), -1)
                        cv2.putText(frame, str(object_id)+coming,
                                    (pt[0], pt[1] - 7), 0, 1, (0, 0, 255), 2)

        # Make a copy of the points
        center_points_prev_frame = center_points_crnt_frame.copy()
        tracking_objects_prev = tracking_objects.copy()
        key = cv2.waitKey(33)
        if key == 27:
            break


cap.release()
cv2.destroyAllWindows()
