import java.util.Scanner; 
 
public class MatrixMultiplication { 
    public static void main(String[] args) { 
        Scanner scanner = new Scanner(System.in); 
 
        // Input dimensions for first matrix 
        System.out.print("Enter number of rows for first matrix: "); 
        int r1 = scanner.nextInt(); 
        System.out.print("Enter number of columns for first matrix: "); 
        int c1 = scanner.nextInt(); 
 
        // Input dimensions for second matrix 
        System.out.print("Enter number of rows for second matrix: "); 
        int r2 = scanner.nextInt(); 

        System.out.print("Enter number of columns for second matrix: "); 
        int c2 = scanner.nextInt(); 
 
        // Check if multiplication is possible 
        if (c1 != r2) { 
            System.out.println("Matrix multiplication not possible. Columns of first matrix must equal rows of second matrix."); 
            scanner.close(); 
            return; 
        } 
 
        int[][] matrix1 = new int[r1][c1]; 
        int[][] matrix2 = new int[r2][c2]; 
        int[][] result = new int[r1][c2]; 
 
        // Input elements of first matrix 
        System.out.println("Enter elements of first matrix:"); 
        for (int i = 0; i < r1; i++) { 
            for (int j = 0; j < c1; j++) { 
                matrix1[i][j] = scanner.nextInt(); 
            } 
        } 
 
        // Input elements of second matrix 
        System.out.println("Enter elements of second matrix:"); 
        for (int i = 0; i < r2; i++) { 
            for (int j = 0; j < c2; j++) { 
                matrix2[i][j] = scanner.nextInt(); 
            } 
        } 
 
        // Multiply matrices 
        for (int i = 0; i < r1; i++) { 
            for (int j = 0; j < c2; j++) { 
                result[i][j] = 0; 
                for (int k = 0; k < c1; k++) { 
                    result[i][j] += matrix1[i][k] * matrix2[k][j]; 
                } 
            } 
        } 
 
        // Display result 
        System.out.println("Product of the matrices:"); 
        for (int i = 0; i < r1; i++) { 
            for (int j = 0; j < c2; j++) { 
                System.out.print(result[i][j] + "\t"); 
            } 
            System.out.println(); 
        } 
 
        scanner.close(); 
    } 
} 
