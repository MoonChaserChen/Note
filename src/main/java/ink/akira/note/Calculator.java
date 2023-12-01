package ink.akira.note;

public class Calculator {
    private IMath math;

    public void calc(int a, int b) {
        System.out.println(math.add(a, b));
        System.out.println(math.subtract(a, b));
    }
}
