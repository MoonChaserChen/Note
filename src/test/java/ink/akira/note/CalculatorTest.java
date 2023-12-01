package ink.akira.note;

import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.MockitoAnnotations;
import org.mockito.junit.MockitoJUnitRunner;

import static org.mockito.Mockito.*;

@RunWith(MockitoJUnitRunner.class)
public class CalculatorTest {
    @Mock
    private IMath math;

    @InjectMocks
    private Calculator calculator;

    @Test
    public void testCalc() {
        when(math.add(anyInt(), anyInt())).thenReturn(10);
        when(math.subtract(anyInt(), anyInt())).thenReturn(20);
        calculator.calc(1, 2);
    }
}
