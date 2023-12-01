# Mockito
假设业务中有以下方法，需要对其进行Mock。
```java
public interface IMath {
    int add(int a, int b);
    int subtract(int a, int b);
}

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
```

## HelloWorld
```java
public class MathTest {
    @Test
    public void testAdd() {
        // 这里是对接口进行Mock，对实体类Mock也可以。
        IMath mockMath = Mockito.mock(IMath.class);
        // Mock方法
        Mockito.when(mockMath.add(Mockito.anyInt(), Mockito.anyInt())).thenReturn(0);
        Assert.assertEquals(0, mockMath.add(1, 2));
        // 未Mock的方法返回默认值（因为默认的defaultAnswer策略是 RETURNS_DEFAULTS）
        Assert.assertEquals(0, mockMath.subtract(1, 2));
    }
}
```
## 两种Mock风格
1. do...when
2. when...then

```java
public class MathTest {
    @Test
    public void testAdd() {
        IMath mockMath = mock(IMath.class);
        /// when...then
        when(mockMath.add(anyInt(), anyInt()))
                .thenReturn(0);
        // do...when
        doReturn(0)
                .when(mockMath)
                .add(anyInt(), anyInt());
        assertEquals(0, mockMath.add(1, 2));
    }
}
```
spy及void方法都需要使用 `do...when` 风格。但我更喜欢 `when...then` 这种风格，下面都以此为例。

## thenCallRealMethod
调用真实方法
```java
public class MathTest {
    @Test
    public void testAdd() {
        IMath mockMath = mock(Math.class);
        when(mockMath.add(anyInt(), anyInt()))
                .thenCallRealMethod();
        assertEquals(3, mockMath.add(1, 2));
    }
}

```
原方法有执行，控制台有以下输出：  
`Real Call Math#add(..). a = 1, b = 2`

`thenCallRealMethod()` 相当于`new Math().add(..)`，因此不能对抽象类及接口Mock。
```java
public class MathTest {
    @Test
    public void testAdd() {
        // 这里用的IMatch进行Mock
        IMath mockMath = mock(IMath.class);
        when(mockMath.add(anyInt(), anyInt()))
                .thenCallRealMethod(); // Calling real methods is only possible when mocking non abstract method.
        assertEquals(3, mockMath.add(1, 2));
    }
}
```

## thenReturn
修改返回值
```java
public class MathTest {
    @Test
    public void testAdd() {
        IMath mockMath = mock(Math.class);
        when(mockMath.add(anyInt(), anyInt()))
                .thenReturn(0);
        assertEquals(0, mockMath.add(1, 2));
    }
}
// 
```
原方法未执行，控制台没有输出。

## doAnswer
修改方法执行
```java
public class MathTest {
    @Test
    public void testAdd() {
        IMath mockMath = mock(Math.class);
        when(mockMath.add(anyInt(), anyInt()))
                .thenAnswer(m -> {
                    System.out.println(m.getMethod().getName());
                    for (Object argument : m.getArguments()) {
                        System.out.println(argument);
                    }
                    // 如果原方法返回值类型是void，这里可以返回null
                    return 0;
                });
        assertEquals(0, mockMath.add(1, 2));
    }
}
```
原方法未执行，控制台有以下输出：  
```
add
1
2
```

## thenThrow
直接抛异常。（在单测里有啥用呢？）
```java
public class MathTest {
    @Test(expected = RuntimeException.class)
    public void testAdd() {
        IMath mockMath = mock(Math.class);
        when(mockMath.add(1, 2))
                .thenThrow(new RuntimeException("Not Allowed"));
        mockMath.add(1, 2);
    }
}
```

## 链式Mock
```java
public class MathTest {
    @Test
    public void testAdd() {
        IMath mockMath = mock(IMath.class);
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
```

## Spy
可以Mock部分方法，未mock的方法调用原方法。 

**Spy需要使用 `do...when` 的风格，如果用 `when...then` 的风格将导致原方法被调用。**
```java
public class MathTest {
    @Test
    public void testAdd() {
        IMath mockMath = spy(Math.class);
        // when(mockMath.add(anyInt(), anyInt())).thenReturn(0); // when...then的方式会导致原方法被调用
        doReturn(0).when(mockMath).add(anyInt(), anyInt());
        assertEquals(0, mockMath.add(1, 2));
        // 未Mock的方法返回默认值
        assertEquals(-1, mockMath.subtract(1, 2));
    }
}
```

## printInvocations
查看调用详情。
```java
public class MathTest {
    @Test
    public void testAdd() {
        IMath mockMath = spy(Math.class);
        doReturn(0).when(mockMath).add(anyInt(), anyInt());
        assertEquals(0, mockMath.add(1, 2));
        assertEquals(-1, mockMath.subtract(1, 2));
        System.out.println(mockingDetails(mockMath).printInvocations());
    }
}
```
控制台输出：
```
[Mockito] Interactions of: ink.akira.note.Math@ab7a938
 1. math.add(1, 2);
  -> at ink.akira.note.MathTest.testAdd(MathTest.java:14)
   - stubbed -> at ink.akira.note.MathTest.testAdd(MathTest.java:13)
 2. math.subtract(1, 2);
  -> at ink.akira.note.MathTest.testAdd(MathTest.java:15)
```

## verify
行为断言，验证某些方法被调用过。是对Junit断言的补充。
```java
public class MathTest {
    @Test
    public void testAdd() {
        // 这里用的IMatch进行Mock
        IMath mockMath = mock(IMath.class);
        for (int i = 0; i < 3; i++) {
            mockMath.add(i, i);
        }
        // 验证 add 方法被执行了3次
        verify(mockMath, times(3)).add(anyInt(), anyInt());
        // 验证 subtract 方法未被执行
        verify(mockMath, never()).subtract(anyInt(), anyInt());

        // 验证调用顺序
        IMath mockMath2 = mock(IMath.class);
        mockMath2.subtract(1, 2);
        InOrder inOrder = inOrder(mockMath2, mockMath); // 这里的参数顺序不重要
        inOrder.verify(mockMath, times(3)).add(anyInt(), anyInt());
        inOrder.verify(mockMath2).subtract(anyInt(), anyInt());
    }
}
```

## @Mock与@Spy
对 `IMath mockMath = mock(IMath.class)` 的简写。但是写在 `test runner` 里，如：`MockitoJUnitRunner`。这样单测可以写得更优雅。
```java
@RunWith(MockitoJUnitRunner.class)
public class MathTest {

    @Mock
    private IMath mockMath;

    @Test
    public void testAdd() {
        when(mockMath.add(anyInt(), anyInt())).thenReturn(0);
        assertEquals(0, mockMath.add(1, 2));
    }
}
```

## @InjectMocks
```java
public class Calculator {
    private IMath math;

    public void calc(int a, int b) {
        System.out.println(math.add(a, b));
        System.out.println(math.subtract(a, b));
    }
}

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
```
控制台输出：
```
10
20
```
`@InjectMocks` 不能加到接口上，这样就不太好用了。


## SpringBoot集成Mockito
```java
@SpringBootTest(classes = Application.class)
@RunWith(SpringRunner.class)
@Slf4j
public class VoucherOperatorRpcServiceTest {
    @Autowired
    private VoucherQueryRpcService voucherQueryRpcService;

    @Autowired
    private VoucherOperatorRpcService voucherOperatorRpcService;

    @MockBean()
    private YuPaoEventReportCollector yuPaoEventReportCollector;

    @MockBean()
    private RedDotRpcService redDotRpcService;

    @MockBean()
    private YuPaoJedis yuPaoJedis;

    @MockBean()
    private ReachRpcService reachRpcService;

    @MockBean()
    private BizMessageRpcService bizMessageRpcService;

    @Test
    @Transactional
    public void testSendVoucher4Task() {
        // 固定任务数据
        Long userId = 1107000000L;
        String templateId = "1726927135668568122";
        String taskId = "1726927967315165244";

        // rpc请求Mock
        mockRpc4TestSendVoucher4Task();

        VoucherTaskSendVoucherReq sendVoucherReq = new VoucherTaskSendVoucherReq();
        sendVoucherReq.setUserId(userId);
        sendVoucherReq.setTemplateId(templateId);
        sendVoucherReq.setTaskId(taskId);

        // 完成任务发券
        Result<VoucherTaskSendVoucherResp> resp = voucherOperatorRpcService.sendVoucher4Task(sendVoucherReq);
        assertThat(resp).isNotNull();
        if (resp.getCode() == 0) {
            assertThat(resp.getData()).isNotNull();
            assertThat(resp.getData().getVoucherInstanceId()).isNotBlank();
            assertThat(resp.getData().getPriceInfo()).isNotNull();

            // 校验发券结果
            VoucherCountByUserRpcReq req = new VoucherCountByUserRpcReq();
            req.setUserId(userId);
            req.setTemplateId(templateId);
            req.setRecentDays(60);
            Result<Integer> integerResult = voucherQueryRpcService.countByUser(req);
            assertThat(integerResult).isNotNull();
            assertThat(integerResult.getData()).isEqualTo(1);
        }
    }

    private void mockRpc4TestSendVoucher4Task() {
        Mockito.doAnswer(m -> {
            log.info("Fake invoke yuPaoEventReportCollector#send");
            return null;
        }).when(yuPaoEventReportCollector).send(any());

        Mockito.doAnswer(m -> {
            log.info("Fake invoke redDotRpcServiceApi#incr");
            return null;
        }).when(redDotRpcService).incr(any());

        when(yuPaoJedis.lpush(anyString(), anyString())).thenAnswer(m -> {
            log.info("Fake invoke yuPaoJedis#lpush");
            return 1L;
        });

        when(yuPaoJedis.setnx(anyString(), anyString())).thenAnswer(m -> {
            log.info("Fake invoke yuPaoJedis#setnx");
            return 1L;
        });

        when(yuPaoJedis.expire(anyString(), anyInt())).thenAnswer(m -> {
            log.info("Fake invoke yuPaoJedis#expire");
            return 1L;
        });

        Mockito.doAnswer(m -> {
            log.info("Fake invoke reachRpcService#sendMessage");
            return null;
        }).when(reachRpcService).sendMessage(any());

        Mockito.doAnswer(m -> {
            log.info("Fake invoke bizMessageRpcService#recordMessage");
            return null;
        }).when(bizMessageRpcService).recordMessage(any());
    }
}
```