## Mock方法执行
```java
public class MyList extends AbstractList<String> {
 
    @Override
    public void add(int index, String element) {
        // no-op
    }
}

public class CommonTest {
    @Test
    public void whenAddCalledAnswered() {
        MyList myList = mock(MyList.class);
        doAnswer(invocation -> {
            Object arg0 = invocation.getArgument(0);
            Object arg1 = invocation.getArgument(1);
            
            assertEquals(3, arg0);
            assertEquals("answer me", arg1);
            return null;
        }).when(myList).add(any(Integer.class), any(String.class));
        myList.add(3, "answer me");
    }
}
```

```java
interface MockI {
    String doSomething();
}

public class CommonTest {
@Test
    public void testMock() {
        final String mockResult = "doSomethingMockResult";
        MockI mock = mock(MockI.class);
        doAnswer(t -> {
            System.out.println("doMockSomething");
            return mockResult;
        }).when(mock).doSomething();
    
        assert mockResult.equals(mock.doSomething());
    }
}
```