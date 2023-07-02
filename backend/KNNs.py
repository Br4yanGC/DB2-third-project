import time
import os
import numpy
import face_recognition
from queue import PriorityQueue 
import pandas as pd
from sklearn.neighbors import KDTree
from rtree import index
import linecache as lc
import json
import io
import cv2

cwd = os.getcwd()

def load_block_dictionary(block_dictionary, total):
    for i in range(1, total):
        PATH = os.path.join(cwd, "feature_vectors.json")
        try:
            aux = lc.getline(PATH, i).rstrip()
            if aux != "":
                json_object = json.load(io.StringIO(aux))
                key = list(json_object.keys())
                value = tuple(json_object.values())
                block_dictionary[key[0]] = value[0]
        except:
            print("There are no processed images")
            return 0
    return block_dictionary


class knn_rtree:
    def __init__(self, p, BD, ID):
        # print(type(self.idx128d))
        self.idx128d = p
        self.block_dictionary = BD
        self.indexed_dictionary = ID

        items =  list(self.block_dictionary.items())
        counter = 1
        for item in items:
            val = tuple(numpy.array(list(map(float, item[1].strip("()").split(', ')))))
            # print("Inserting point " + str(counter))
            self.idx128d.insert(counter, val)
            self.indexed_dictionary[counter] = (str(item[0]), val)
            counter += 1

    def knn_search_rtree(self, file_name, K, cwd, indexed_dictionary,idx):
        image_path = os.path.join(cwd, file_name)
        if not os.path.exists(image_path):
            print("No path")
            return [0, 0]
        else:
            face = face_recognition.load_image_file(image_path)
            face_encoding = face_recognition.face_encodings(face) # calculating the image encoding
            if len(face_encoding) == 0:
                print("no face found")
                return [0, 0]
            else:
                new_face_encoding = tuple(face_encoding[0])
                result=[]
                print("searching...")
                start=time.time()
                KNNvalue = list(idx.nearest(coordinates=new_face_encoding, num_results=K))
                end=time.time()     
                counter = 1
                for idx in KNNvalue:
                    item = indexed_dictionary[idx]
                    path = item[0]
                    first = numpy.array(item[1])
                    second = numpy.array(new_face_encoding[0])
                    distance = numpy.linalg.norm(first - second)
                    # if(previous_path != path):
                    result.append((path, round(distance, 3)))
                    # previous_path = path
                    if counter > K:
                        break
                    counter += 1
                
                execution_time = round((end - start) * 1000, 3)
                print("knn search rtree search took " + str(execution_time) + " ms.")
                return [result, execution_time]

    def range_search_rtree(self, file_name, radius, cwd, idx, indexed_dictionary):
        image_path = os.path.join(cwd, file_name)
        if not os.path.exists(image_path):
            print("No path")
            return[0, 0]
        else:
            face = face_recognition.load_image_file(image_path)
            face_encoding = face_recognition.face_encodings(face) # calculating the image encoding
            if len(face_encoding) == 0:
                print("no face found")
                return [0, 0]
            else:
                new_face_encoding = tuple(face_encoding[0])
                limite_inferior = []
                limite_superior = []
                for point in new_face_encoding:
                    limite_inferior.append(point - radius)
                    limite_superior.append(point + radius)
                bound = limite_inferior + limite_superior
                start = time.time()
                range_values = [n for n in idx.intersection(bound)]
                end = time.time()
                result = []
                second = numpy.array(new_face_encoding[0])
                previous_path = ""
                for idx in range_values:
                    # dist = numpy.linalg.norm(numpy.asarray(new_face_encoding)-numpy.asarray(vectors[path]))
                    item = indexed_dictionary[idx]
                    path = item[0]
                    first = numpy.array(item[1])
                    dist = numpy.linalg.norm(first - second)
                    if dist < radius and path != previous_path:
                        result.append((path, round(dist, 3)))
                    previous_path = path
                # result = sorted(result, key=lambda item: item[2])

                execution_time = round((end - start) * 1000, 3)
                print("range search rtree took " + str(execution_time) + " ms.")
                return [result, execution_time]


class knn_kdtree:
    def kdtree(file_name, k, cwd, block_dictionary):
        image_path = os.path.join(cwd, file_name)
        if not os.path.exists(image_path):
            print("No path")
            return [0, 0]
        else:
            face = face_recognition.load_image_file(image_path)
            face_encoding = face_recognition.face_encodings(face)
            face_encoding = numpy.array(face_encoding)
            if len(face_encoding) == 0:
                print("no face founnd")
                return [0, 0]
            else:

                isFile = os.path.isfile(cwd+'/KD-TREE.csv')
                
                if not isFile:
                    # print("a")
                    # Tener todo en un dataframe
                    col = [str(i) for i in range(128)]
                    temp1 = pd.DataFrame(columns=col)
                    img = pd.DataFrame(columns=["img"])
                    for path in block_dictionary:
                        first = numpy.array(list(map(float, block_dictionary[path].strip("()").split(', '))))
                        first = pd.DataFrame(first.reshape(1,-1), columns=list(col))
                        temp1 = pd.concat( [temp1, first]) 
                        second = pd.DataFrame(numpy.array([path]), columns=["img"])
                        img = pd.concat([img,second])
                    temp1["img"] = img
                    time1 = time.time()
                    temp1.to_csv(cwd+'/KD-TREE.csv',index=False, encoding='utf-8')    
                    temp1.reset_index(drop=True, inplace=True)
                    tree = KDTree(temp1.iloc[:, 0:-1])
                    dist, ind = tree.query(face_encoding,k)
                    result = []
                    for i in range(len(dist[0])):
                        result.append((temp1.iloc[ind[0][i]].values.tolist()[-1], round(dist[0][i],3)))
                    time2 = time.time()

                    execution_time = round((time2 - time1) * 1000)
                    print("kdtree took " + str(execution_time) + " ms.")
                    return [result, execution_time]
                else:
                    print("searching...")
                    time1 = time.time()
                    #temp1.to_csv('KD-TREE.csv',index=False, encoding='utf-8')    
                    temp1 = pd.read_csv(cwd+'/KD-TREE.csv')
                    temp1.reset_index(drop=True, inplace=True)
                    tree = KDTree(temp1.iloc[:, 0:-1])
                    dist, ind = tree.query(face_encoding,k)
                    result = []
                    for i in range(len(dist[0])):
                        result.append((temp1.iloc[ind[0][i]].values.tolist()[-1], round(dist[0][i],3)))
                    time2 = time.time()

                    execution_time = round((time2 - time1) * 1000)
                    print("kdtree took " + str(execution_time) + " ms.")
                    return [result, execution_time]
                

    def live_kdtree(k, cwd):
        video_capture = cv2.VideoCapture(0)
        process_this_frame = True

        while True:
            ret, frame = video_capture.read()

            if process_this_frame:
                if ret == False: 
                    break
                frame = cv2.flip(frame, 1)
                frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

                # face_locations = face_recognition.face_locations(frame)
                face_locations = face_recognition.face_locations(frame, model="cnn")
                if face_locations != []:
                    for face_location in face_locations:
                        top, right, bottom, left = face_location
                        face_encoding = face_recognition.face_encodings(frame, known_face_locations=[face_location])[0]
                        
                        face_encoding = numpy.array(face_encoding).reshape(1, -1)

                        best_match = "Quien eres?"
                        color = (0, 0 ,255) #red

                        temp1 = pd.read_csv(cwd+'/KD-TREE.csv')
                        temp1.reset_index(drop=True, inplace=True)
                        tree = KDTree(temp1.iloc[:, 0:-1])
                        dist, ind = tree.query(face_encoding, k)
                        best_dist = round(dist[0][0], 3)

                        if best_dist < 0.55:
                            best_match = temp1.iloc[ind[0][0]].values.tolist()[-1]
                            color = (0, 255, 0) # green
                        
                        text = best_match + " - " + str(best_dist)

                        # Draw bounding box around the face and display name
                        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
                        cv2.putText(frame, text, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.25, color, 1)
                        print(text)

                cv2.imshow("Face Recognition", frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            
            process_this_frame = not process_this_frame
        
        video_capture.release()
        cv2.destroyAllWindows()


class knn_seq:
    def range_search(file_name, radius, cwd, block_dictionary):
        image_path = os.path.join(cwd, file_name)
        if not os.path.exists(image_path):
            print("No path")
            return [0, 0]
        else:
            face = face_recognition.load_image_file(image_path)
            face_encoding = face_recognition.face_encodings(face) # calculating the image encoding
            if len(face_encoding) == 0:
                print("no face founnd")
                return [0, 0]
            else:
                new_face_encoding = tuple(face_encoding)
                result = []
                #gather info
                info = []
                print("searching...")
                time1 = time.time()
                # for i in range(total):
                for path in block_dictionary:

                    first = numpy.array(list(map(float, block_dictionary[path].strip("()").split(', '))))
                    second = numpy.array(list(map(float, new_face_encoding[0])))
                    distance = numpy.linalg.norm(first - second)
                    if distance < radius:
                        result.append((path, distance))
                        person = path
                        info.append((person, round(distance,3)))
                time2 = time.time()

                execution_time = round((time2 - time1) * 1000)
                print("range_search took " + str(execution_time) + " ms.")
                return [info, execution_time]

    def knn_search(file_name, k, cwd, block_dictionary):
        pq = PriorityQueue(False)
        image_path = os.path.join(cwd, file_name)
        if not os.path.exists(image_path):
            print("No path")
            return [0, 0]
        else:
            face = face_recognition.load_image_file(image_path)
            face_encoding = face_recognition.face_encodings(face) # calculating the image encoding
            if len(face_encoding) == 0:
                print("no face found")
                return [0, 0]
            else:
                new_face_encoding = tuple(face_encoding)
                result = []
                #gather info
                # info = []
                print("searching...")
                time1 = time.time()
                for path in block_dictionary:
                    first = numpy.array(list(map(float, block_dictionary[path].strip("()").split(', '))))
                    second = numpy.array(list(map(float, new_face_encoding[0])))
                    distance = numpy.linalg.norm(first - second)
                    person = path
                    pq.put((person, round(distance,3)))
                    # info.append((person, round(distance,3)))
                for i in range(k):
                    result.append(pq.get())
                time2 = time.time()

                execution_time = round((time2 - time1) * 1000)
                print("knn_search took " + str(execution_time) + " ms.")
                return [result, execution_time]