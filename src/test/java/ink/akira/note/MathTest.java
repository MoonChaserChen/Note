package ink.akira.note;

import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.InOrder;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;

import static org.junit.Assert.assertEquals;
import static org.mockito.Mockito.*;

public class MathTest {
    @Test
    public void testAdd() {
        Math mockMath = mock(Math.class);
        when(mockMath.add(1, 2))
                // 第1次调用返回0
                .thenReturn(0)
                // 第2次及以后调用返回1
                .thenReturn(1);
        assertEquals(0, mockMath.add(1, 2));
        assertEquals(1, mockMath.add(1, 2));
        assertEquals(1, mockMath.add(1, 2));
    }
}
