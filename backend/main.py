from image_processing import *
from KNNs import *
import os

cwd = os.getcwd()
processed_images = os.path.join(cwd, "feature_vectors.json")

if not os.path.exists(processed_images):
    process_dataset()

def printing(info):
    counter = 0
    for key in info[0]:
        print(str(counter) + ") -> (" + str(key[0]) + ", " + str(key[1]) + ")")
        counter += 1

class Indexacion_Busqueda:
    total = 13175
    block_dictionary = {}
    indexed_dictionary = {}    

    def __init__(self):
        if(len(self.block_dictionary) == 0):
            self.block_dictionary = load_block_dictionary(self.block_dictionary, self.total)
        p = index.Property()
        p.dimension = 128 
        p.buffering_capacity = 4
        p.dat_extension = 'data'
        p.idx_extension = 'index'
        self.idx128d = index.Index('128d_index', properties=p)
        self.KNN_sequencial  = knn_seq
        self.KNN_RTree       = knn_rtree(self.idx128d, self.block_dictionary, self.indexed_dictionary)
        self.KNN_KDTree      = knn_kdtree
    
    def delete_files(self):
        file_path = os.path.join(cwd, "128d_index.data")
        file_path2 = os.path.join(cwd, "128d_index.index")
        try:
            self.block_dictionary = {}
            self.indexed_dictionary = {}
            os.remove(file_path)
            os.remove(file_path2)
            print(f"The file '{file_path}' has been deleted successfully.")
            print(f"The file '{file_path2}' has been deleted successfully.")
        except OSError as e:
            print(f"Error occurred while deleting the file: {e}")

    def RANGE_SEARCH(self, file_name, radius):
        info = self.KNN_sequencial.range_search(file_name, radius, cwd, self.block_dictionary)
        return info

    def KNN_SEARCH(self, file_name, k):
        info = self.KNN_sequencial.knn_search(file_name, k, cwd, self.block_dictionary)
        return info

    def RANGE_SEARCH_RTREE(self, file_name, radius):
        info = self.KNN_RTree.range_search_rtree(file_name, radius, cwd, self.idx128d, self.indexed_dictionary)
        return info

    def KNN_SEARCH_RTREE(self, file_name, k):
        info = self.KNN_RTree.knn_search_rtree(file_name, k, cwd, self.indexed_dictionary, self.idx128d)
        return info  

    def KDTREE(self, file_name, k):
        info = self.KNN_KDTree.kdtree(file_name, k, cwd, self.block_dictionary)
        return info

def knn_seq_range_search_exec(query_image, radius):
    smt = Indexacion_Busqueda()
    result = smt.RANGE_SEARCH(query_image, radius)
    smt.delete_files()
    return result 

def knn_seq_knn_search_exec(query_image, knn):
    smt = Indexacion_Busqueda()
    result = smt.KNN_SEARCH(query_image, knn)
    smt.delete_files()
    return result

def knn_rtree_range_search_exec(query_image, radius):
    smt = Indexacion_Busqueda()
    result = smt.RANGE_SEARCH_RTREE(query_image, radius)
    smt.delete_files()
    return result

def knn_rtree_knn_search_exec(query_image, knn):
    smt = Indexacion_Busqueda()
    result = smt.KNN_SEARCH_RTREE(query_image, knn)
    smt.delete_files()
    return result

def knn_kdtree_knn_search_exec(query_image, knn):
    smt = Indexacion_Busqueda()
    result = smt.KDTREE(query_image, knn)
    smt.delete_files()
    return result

def knn_kdtree_knn_search_live_exec():
        kdtree = knn_kdtree
        kdtree.live_kdtree(8, cwd)

def live_test():
        kdtree = knn_kdtree
        kdtree.live_kdtree(8, cwd)


#knn_kdtree_knn_search_live_exec()