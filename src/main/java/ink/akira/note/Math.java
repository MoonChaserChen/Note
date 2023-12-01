package ink.akira.note;

public class Math implements IMath {
    @Override
    public int add(int a, int b) {
        System.out.printf("Real Call Math#add(..). a = %d, b = %d%n", a, b);
        return a + b;
    }

    @Override
    public int subtract(int a, int b) {
        return a - b;
    }
}
