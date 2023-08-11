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

doCallRealMethod().when(instance).voidFunction();

**Spring Boot集成mockito，@MockBean**


mock方法和spy方法都可以对对象进行mock。但是前者是接管了对象的全部方法，而后者只是将有桩实现（stubbing）的调用进行mock，其余方法仍然是实际调用。
> 那么@Spy可以用于抽象类或接口么？

when(...) thenReturn(...) 做了真实调用。只是返回了指定的结果

doReturn(...) when(...) 不做真实调用

doAnswer 可以修改执行&返回值， doReturn 可以修改返回值？  
