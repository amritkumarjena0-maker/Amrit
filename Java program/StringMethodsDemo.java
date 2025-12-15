public class StringMethodsDemo {
    public static void main(String[] args) {
        String str = " Hello, java world! ";
        String str2 ="HELLO JAVA WORLD!";
        System.out.println("length: " + str.length());
        String trimmed = str.trim();
        System.out.println("Trimmed: ' " + trimmed + " ' ");
        System.out.println("Uppercase: " + trimmed.toUpperCase());
        System.out.println("Lowercase: " + trimmed.toLowerCase());
        String welcome = "Welcome ";
        System.out.println("Concatenation: " + welcome.concat(trimmed));
        System.out.println("Character at index 1: " + trimmed.charAt(1));
        System.out.println("Substring (7,11): " + trimmed.substring(7,11));
        System.out.println("Equals str2: " + trimmed.equals(str2));
        System.out.println("Equals Ignore Case str2: " + trimmed.equalsIgnoreCase(str2));
        String[] words = trimmed.split(" ");
        System.out.println("Split by space:");
        for (String word : words) {
            System.out.println(word);
        }
    }
}
