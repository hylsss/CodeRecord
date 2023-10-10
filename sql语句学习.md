#### SQL执行顺序

- 我们先执行from,join来确定表之间的连接关系，得到初步的数据
- where对数据进行普通的初步的筛选
- group by 分组
- 各组分别执行having中的普通筛选或者聚合函数筛选。
- 然后把再根据我们要的数据进行select，可以是普通字段查询也可以是获取聚合函数的查询结果，如果是集合函数，select的查询结果会新增一条字段
- 将查询结果去重distinct
- 最后合并各组的查询结果，按照order by的条件进行排序

![微信图片_20231010195233](https://github.com/hylsss/CodeRecord/assets/62007319/c9a36c83-9ba7-4b0c-b80e-62e6ba6590f5)



以员工表和薪资表为例

![640](https://github.com/hylsss/CodeRecord/assets/62007319/c7a8b332-51cb-46df-9d49-525b49a40788)




### **from&&join**
选择一个表使用**join**连接，基于某个共同的字段（在这里是 `id`）进行连接

```sql
from employee join salary on employee.id=salary.id
```
`只有在两个表中都存在的 id 值才会出现在结果集中`。如果 employee 表中有一个 id 值，在 salary 表中没有对应的 id 值（或反之），那么**这个 id 值不会出现在结果集中**。

### **where**
选择多张表，用**where**做关联条件，也是连接两张表。
```sql
from employee,salary where employee.id=salary.id
```

###  group by && having
按照我们的分组条件，将数据进行分组，但是不会筛选数据。
例如按照奇偶分组
id%2=0
id%2=1
`having` 可以使用普通条件进行筛选，也可以使用`聚合函数`进行筛选。`having` 子句通常与 `group by`一起使用，以对分组后的数据进行筛选。

##### 聚合函数是 SQL 中的一类特殊函数，用于对数据进行汇总或计算。以下是一些常见的聚合函数：
1. COUNT(): 计算某列的行数。例如，COUNT(id) 会计算 id 列的行数。
2. SUM(): 计算某列的总和。例如，SUM(salary) 会计算 salary 列的总和。
3. AVG(): 计算某列的平均值。例如，AVG(salary) 会计算 salary 列的平均值。
4. MAX(): 返回某列的最大值。例如，MAX(salary) 会返回 salary 列的最大值。
5. MIN(): 返回某列的最小值。例如，MIN(salary) 会返回 salary 列的最小值。
6. GROUP_CONCAT() (在某些数据库系统中): 用于连接多个列值。例如，GROUP_CONCAT(name) 会连接所有的 name 列值

```SQL
SELECT department, AVG(salary) AS avg_salary
FROM employees
WHERE department IN ('IT', 'Finance')
GROUP BY department
HAVING AVG(salary) > 50000;

//查询的结果会返回那些在 "IT" 和 "Finance" 部门中，平均薪水超过 50000 的部门名称和它们的平均薪水。
```

#### select

```sql
// 选择指定的列
SELECT column1 ,column2 FROM table_name

// 选择所有的列
SELECT * FROM table_name

// DISTINCT: 这个关键字确保查询结果中的每个 id 值都是唯一的，即它会去除任何重复的 id 值。
SELECT DISTINCT employee.id FROM employee

// 只有满足条件的记录才会被选中,where在这里用来过滤结果
SELECT column1,column2 FROM table_name WHERE condition

// ORDER BY 子句用于对结果进行排序。默认是升序 (ASC)，如果想要降序可以使用 DESC。
SELECT column1,column2 FROM table_name ORDER BY column1 , columm2 ASC;
```

![微信图片_20231010195223](https://github.com/hylsss/CodeRecord/assets/62007319/eb1c0451-1c0f-4ce3-82a8-97103aff55ad)

#### limit

`OFFSET` 关键字用于指定开始选择记录的位置
```sql
// 返回前n条数据
SELECT column1 ,column2 FROM table_name LIMIT number;

//LIMIT 5 OFFSET 10 会跳过前 10 条记录，并返回接下来的 5 条记录。
SELECT column1,column2 FROM table_name LIMIT number OFFSET number; 
```
**常见用途**:
- **分页**: 当你有大量数据需要在网页上分页显示时，`LIMIT` 和 `OFFSET` 可以帮助你每次只获取一页的数据。
- **随机样本**: 在某些数据库系统中，你可以结合 `ORDER BY` 使用 `LIMIT` 来获取随机样本。例如：`SELECT column FROM table_name ORDER BY RAND() LIMIT 5;`。


