import matplotlib.pyplot as plt
from sklearn.impute import KNNImputer
from utils import *


def knn_impute_by_user(matrix, valid_data, k):
    """ Fill in the missing values using k-Nearest Neighbors based on
    student similarity. Return the accuracy on valid_data.

    See https://scikit-learn.org/stable/modules/generated/sklearn.
    impute.KNNImputer.html for details.

    :param matrix: 2D sparse matrix
    :param valid_data: A dictionary {user_id: list, question_id: list,
    is_correct: list}
    :param k: int
    :return: float
    """
    nbrs = KNNImputer(n_neighbors=k)
    # We use NaN-Euclidean distance measure.
    mat = nbrs.fit_transform(matrix)
    acc = sparse_matrix_evaluate(valid_data, mat)
    print("Validation Accuracy: {}".format(acc))
    return acc


def knn_impute_by_item(matrix, valid_data, k):
    """ Fill in the missing values using k-Nearest Neighbors based on
    question similarity. Return the accuracy on valid_data.

    :param matrix: 2D sparse matrix
    :param valid_data: A dictionary {user_id: list, question_id: list,
    is_correct: list}
    :param k: int
    :return: float
    """
    #####################################################################
    # TODO:                                                             #
    # Implement the function as described in the docstring.             #
    #####################################################################
    matrix_transposed = matrix.T
    nbrs = KNNImputer(n_neighbors=k)
    mat_transposed = nbrs.fit_transform(matrix_transposed)
    mat = mat_transposed.T
    acc = sparse_matrix_evaluate(valid_data, mat)
    #####################################################################
    #                       END OF YOUR CODE                            #
    #####################################################################
    return acc


def main():
    sparse_matrix = load_train_sparse("../data").toarray()
    val_data = load_valid_csv("../data")
    test_data = load_public_test_csv("../data")

    print("Sparse matrix:")
    print(sparse_matrix)
    print("Shape of sparse matrix:")
    print(sparse_matrix.shape)

    #####################################################################
    # TODO:                                                             #
    # Compute the validation accuracy for each k. Then pick k* with     #
    # the best performance and report the test accuracy with the        #
    # chosen k*.                                                        #
    #####################################################################
    best_k = None
    best_val_acc = 0

    all_val_acc = []

    k_values = [1, 6, 11, 16, 21, 26]

    for k in k_values:
        val_acc = knn_impute_by_user(sparse_matrix, val_data, k)
        all_val_acc.append(val_acc)
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            best_k = k

    plt.plot(k_values, all_val_acc, marker='o')
    plt.xlabel('k')
    plt.ylabel('Validation Accuracy')
    plt.title('Validation Accuracy vs k')
    plt.grid(True)
    plt.show()

    plt.savefig('validation_accuracy_plot.png', dpi=300)

    test_acc = knn_impute_by_user(sparse_matrix, test_data, best_k)
    print("k value selected:", best_k)
    print("Test accuracy with best k:", test_acc)
    #####################################################################
    #                       END OF YOUR CODE                            #
    #####################################################################


if __name__ == "__main__":
    main()
