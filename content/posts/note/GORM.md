---
title: "GORM学习"
date: 2022-02-10
description: "GORM学习"
featured : false
categories: ["notes"]
tags: [ "gorm" ]
images: []
---

### GORM

#### 模型定义

1. 模型实现了Scanner和Valuer接口

2. 模型约定：

    - GORM 使用`ID`作为主键

        - 如果不默认使用`ID`作为主键，应该使用标签`primaryKey` 指定

            - ```go
                // 将 `UUID` 设为主键
                type Animal struct {
                  ID     int64
                  UUID   string `gorm:"primaryKey"`
                  Name   string
                  Age    int64
                }
                ```

        - 复合主键

            - ```go
                type Product struct {
                  ID           string `gorm:"primaryKey"`
                  LanguageCode string `gorm:"primaryKey"`
                  Code         string
                  Name         string
                }
                ```

        - 关闭整形主键的自增，显示关闭 `autoIncrement`

            - ```go
                type Product struct {
                  CategoryID uint64 `gorm:"primaryKey;autoIncrement:false"`
                  TypeID     uint64 `gorm:"primaryKey;autoIncrement:false"`
                }
                ```

    - 使用结构体名的**下划线表示的复数**作为表名

        - 更改默认表名,为结构体实现`TableName`方法

            - ```go
                type Tabler interface {
                    TableName() string
                }
                
                // TableName 会将 User 的表名重写为 `profiles`
                func (User) TableName() string {
                  return "profiles"
                }
                ```

        - 动态修改表名：使用`Scopes`

            - 用`Scopes`来动态添加条件

                - ```go
                    func UserTable(user User) func (tx *gorm.DB) *gorm.DB {
                      return func (tx *gorm.DB) *gorm.DB {
                        if user.Admin {
                          return tx.Table("admin_users")
                        }
                    
                        return tx.Table("users")
                      }
                    }
                    
                    db.Scopes(UserTable(user)).Create(&user)
                    ```

        - 临时指定表名，使用`Table`方法临时指定表名

            - ```go
                // 根据 User 的字段创建 `deleted_users` 表
                db.Table("deleted_users").AutoMigrate(&User{})
                ```

        - 修改默认的命名策略：实现结构体的命名相关的接口

            - `TableName`、`ColumnName`、`JoinTableName`、`RelationshipFKName`、`CheckerName`、`IndexName`等接口

    - 使用字段名的**下划线表示**作为列名

        - 使用`column`标签或者`命名策略` 来指定列名

            - ```go
                type Animal struct {
                  AnimalID int64  `gorm:"column:beast_id"`         // 将列名设为 `beast_id`
                  Birthday time.Time `gorm:"column:day_of_the_beast"` // 将列名设为 `day_of_the_beast`
                  Age      int64     `gorm:"column:age_of_the_beast"` // 将列名设为 `age_of_the_beast`
                }
                ```

    - 使用`CreatedAt`、`UpdatedAt` 字段追踪创建、更新时间

        - CreatedAt字段的修改规则

            - ```go
                db.Create(&user) // 将 `CreatedAt` 设为当前时间
                
                user2 := User{Name: "jinzhu", CreatedAt: time.Now()}
                db.Create(&user2) // user2 的 `CreatedAt` 不会被修改
                
                // 想要修改该值，您可以使用 `Update`
                db.Model(&user).Update("CreatedAt", time.Now())
                ```

        - UpdateAt字段的修改规则

            - ```go
                db.Save(&user) // 将 `UpdatedAt` 设为当前时间
                
                db.Model(&user).Update("name", "jinzhu") // 会将 `UpdatedAt` 设为当前时间
                
                db.Model(&user).UpdateColumn("name", "jinzhu") // `UpdatedAt` 不会被修改
                
                user2 := User{Name: "jinzhu", UpdatedAt: time.Now()}
                db.Create(&user2) // 创建记录时，user2 的 `UpdatedAt` 不会被修改
                
                user3 := User{Name: "jinzhu", UpdatedAt: time.Now()}
                db.Save(&user3) // 更新时，user3 的 `UpdatedAt` 会修改为当前时间
                ```

    - `gorm.Model`默认的结构体，包含了默认的字段

        - 定义

            - ```go
                // gorm.Model 的定义
                type Model struct {
                  ID        uint           `gorm:"primaryKey"`
                  CreatedAt time.Time
                  UpdatedAt time.Time
                  DeletedAt gorm.DeletedAt `gorm:"index"`
                }
                ```

        - 可以嵌入到自己的结构体中以包含这些默认字段

    - 时间相关约定

        - 类型约定

            - `time.Time`，时间类型

            - `int`，时间戳秒数

            - `int64`，默认为时间戳秒数

                - ```go
                      Updated  int64 `gorm:"autoUpdateTime:nano"` //使用时间戳填纳秒数充更新时间
                      Updated  int64 `gorm:"autoUpdateTime:milli"` //使用时间戳毫秒数填充更新时间
                      Created  int64 `gorm:"autoCreateTime"`      //使用时间戳秒数填充创建时间
                  ```

    - 结构体嵌入

        - 匿名字段

            - ```go
                type User struct {
                  gorm.Model
                  Name string
                }
                // 等效于
                type User struct {
                  ID        uint           `gorm:"primaryKey"`
                  CreatedAt time.Time
                  UpdatedAt time.Time
                  DeletedAt gorm.DeletedAt `gorm:"index"`
                  Name string
                }
                ```

        - 具名字段，使用标签`embedded`嵌入

            - ```go
                type Author struct {
                    Name  string
                    Email string
                }
                
                type Blog struct {
                  ID      int
                  Author  Author `gorm:"embedded"`
                  Upvotes int32
                }
                // 等效于
                type Blog struct {
                  ID    int64
                    Name  string
                    Email string
                  Upvotes  int32
                }
                ```

            - 资源前缀修改,`embeddedPrefix`标签

                - ```go
                    type Blog struct {
                      ID      int
                      Author  Author `gorm:"embedded;embeddedPrefix:author_"`
                      Upvotes int32
                    }
                    // 等效于
                    type Blog struct {
                      ID          int64
                        AuthorName  string
                        AuthorEmail string
                      Upvotes     int32
                    }
                    ```

    - [字段标签](https://learnku.com/docs/gorm/v2/models/9729#f87336#%E5%AD%97%E6%AE%B5%E6%A0%87%E7%AD%BE)

    - [关联标签](https://learnku.com/docs/gorm/v2/associations/9740#tags)

#### 数据库连接

##### 数据库驱动以及连接

 - MYSQL

     - [mysql高级配置](https://github.com/go-gorm/mysql)

     - ```go
        import (
          "gorm.io/driver/mysql"
          "gorm.io/gorm"
        )
        
        func main() {
          // 参考 https://github.com/go-sql-driver/mysql#dsn-data-source-name 获取详情
          dsn := "user:pass@tcp(127.0.0.1:3306)/dbname?charset=utf8mb4&parseTime=True&loc=Local"
          db, err := gorm.Open(mysql.Open(dsn), &gorm.Config{})
        }
        ```

 - PostgreSQL

     - [postgre高级配置](https://github.com/go-gorm/postgres)

    - ```go
        import (
          "gorm.io/driver/postgres"
          "gorm.io/gorm"
        )
        
        dsn := "user=gorm password=gorm dbname=gorm port=9920 sslmode=disable TimeZone=Asia/Shanghai"
        db, err := gorm.Open(postgres.Open(dsn), &gorm.Config{})
        ```

- SQLite

    - ```go
        import (
          "gorm.io/driver/sqlite"
          "gorm.io/gorm"
        )
        
        // github.com/mattn/go-sqlite3
        db, err := gorm.Open(sqlite.Open("gorm.db"), &gorm.Config{})
        ```

- SQL Server

    - ```go
        import (
          "gorm.io/driver/sqlserver"
          "gorm.io/gorm"
        )
        
        // github.com/denisenkom/go-mssqldb
        dsn := "sqlserver://gorm:LoremIpsum86@localhost:9930?database=gorm"
        db, err := gorm.Open(sqlserver.Open(dsn), &gorm.Config{})
        ```


##### 数据库连接池

- [*sql.DB](https://pkg.go.dev/database/sql#DB)

- ```go
    // 获取通用数据库对象 sql.DB，然后使用其提供的功能
    sqlDB, err := db.DB()
    
    // Ping
    sqlDB.Ping()
    
    // Close
    sqlDB.Close()
    
    // 返回数据库统计信息
    sqlDB.Stats()
    ```

- ```go
    sqlDB, err := db.DB()
    
    // SetMaxIdleConns 设置空闲连接池中连接的最大数量
    sqlDB.SetMaxIdleConns(10)
    
    // SetMaxOpenConns 设置打开数据库连接的最大数量。
    sqlDB.SetMaxOpenConns(100)
    
    // SetConnMaxLifetime 设置了连接可复用的最大时间。
    sqlDB.SetConnMaxLifetime(time.Hour)
    ```

#### 对象生命周期

Hook 是在创建、查询、更新、删除等操作之前、之后调用的函数。

如果您已经为模型定义了指定的方法，它会在创建、更新、查询、删除时自动被调用。如果任何回调返回错误，GORM 将停止后续的操作并回滚事务。

#### CRUD

##### 创建

- 创建记录

    ```go
    user := User{Name: "Jinzhu", Age: 18, Birthday: time.Now()}
    
    result := db.Create(&user) // 通过数据的指针来创建
    
    user.ID             // 返回插入数据的主键
    result.Error        // 返回 error
    result.RowsAffected // 返回插入记录的条数
    ```

    - 将数据对象的制作传递给`Create`方法来进行创建
    - 方法将会返回error以及插入的条数，同时数据对象的ID字段将会被回写

- 插入指定的字段

    ```go
    db.Select("Name", "Age", "CreatedAt").Create(&user)
    // INSERT INTO `users` (`name`,`age`,`created_at`) VALUES ("jinzhu", 18, "2020-07-04 11:05:21.775")
    ```

    - 创建记录，并且将选择的字段更新

    ```go
    db.Omit("Name", "Age", "CreatedAt").Create(&user)
    // INSERT INTO `users` (`birthday`,`updated_at`) VALUES ("2020-01-01 00:00:00.000", "2020-07-04 11:05:21.775")
    ```

    - 创建记录，并且更新未给出的字段

- **批量插入**:使用`slice`传递给Create方法

    ```go
    var users = []User{{Name: "jinzhu1"}, {Name: "jinzhu2"}, {Name: "jinzhu3"}}
    db.Create(&users)
    for _, user := range users {
      user.ID // 1,2,3
    }
    ```

- **批量插入**:使用 `CreateInBatches` 创建，并支持**指定创建的数量**

    ```go
    var users = []User{name: "jinzhu_1"}, ...., {Name: "jinzhu_10000"}}
    // 数量为 100
    db.CreateInBatches(users, 100)
    ```

- 对象Hook

    - 生命周期

        ```go
        // 开始事务
        BeforeSave
        BeforeCreate
        // 关联前的 save
        // 插入记录至 db
        // 关联后的 save
        AfterCreate
        AfterSave
        // 提交或回滚事务
        ```

    - 跳过Hook，使用`SkipHooks` 会话模式

        ```go
        DB.Session(&gorm.Session{SkipHooks: true}).Create(&user)
        ```

- 根据 `map[string]interface{}` 和 `[]map[string]interface{}{}` 创建记录

    - ```go
        db.Model(&User{}).Create(map[string]interface{}{
          "Name": "jinzhu", "Age": 18,
        })
        
        // batch insert from `[]map[string]interface{}{}`
        db.Model(&User{}).Create([]map[string]interface{}{
          {"Name": "jinzhu_1", "Age": 18},
          {"Name": "jinzhu_2", "Age": 20},
        })
        ```

- 使用`clause.Expr`创建记录

    - ```go
        // 通过 map 创建记录
        db.Model(User{}).Create(map[string]interface{}{
          "Name": "jinzhu",
          "Location": clause.Expr{SQL: "ST_PointFromText(?)", Vars: []interface{}{"POINT(100 100)"}},
        })
        // INSERT INTO `users` (`name`,`point`) VALUES ("jinzhu",ST_PointFromText("POINT(100 100)"));
        ```

- 关联创建

    - 如果两个数据结构有关联，那么在会把关联对象一起upsert

        ```go
        type CreditCard struct {
          gorm.Model
          Number   string
          UserID   uint
        }
        
        type User struct {
          gorm.Model
          Name       string
          CreditCard CreditCard
        }
        
        db.Create(&User{
          Name: "jinzhu",
          CreditCard: CreditCard{Number: "411111111111"}
        })
        // INSERT INTO `users` ...
        // INSERT INTO `credit_cards` ...
        ```

    - skip 关联创建

        ```go
        db.Omit("CreditCard").Create(&user)
        // 跳过所有关联
        db.Omit(clause.Associations).Create(&user)
        ```

- 默认值,可以是值，也可以是数据库函数

    - 使用标签 `default` 为字段定义默认值

        ```go
        type User struct {
          gorm.Mode
          Name 		string 			`gorm:"default:galeone"`
          Weight  	int64  			`gorm:"default:18"`
          Age  		*int       		`gorm:"default:18"`
          Active 	sql.NullBool 	`gorm:"default:true"`
        }
        ```

        - 像 `0`、`''`、`false` 等零值，不会将这些字段定义的默认值保存到数据库。需要使用指针类型或 Scanner/Valuer 来避免这个问题

    - 当具有生成数据时，必须设置`default`标签

        ```go
        type User struct {
          ID        string `gorm:"default:uuid_generate_v3()"` // 数据库函数
          FirstName string
          LastName  string
          Age       uint8
          FullName  string `gorm:"->;type:GENERATED ALWAYS AS (concat(firstname,' ',lastname));default:(-);`
        }
        ```

- Upsert及其冲突，[相关链接](https://learnku.com/docs/gorm/v2/create/9732#f43bde#Upsert及冲突)

    - 出现冲突时，一般分为**DoNothing**，**DoUpdates**，**UpdateAll**

##### 查询

- 检索单个对象

    - `First`函数，按照主键升序获取第一条记录

        ```go
        // 获取第一条记录（主键升序）
        db.First(&user)
        // SELECT * FROM users ORDER BY id LIMIT 1;
        ```

        

    - `Take`函数，不指定排序字段，获取第一条记录

        ```go
        // 获取一条记录，没有指定排序字段
        db.Take(&user)
        // SELECT * FROM users LIMIT 1;
        ```

        

    - `Last`函数，按照主键降序，获取第一条记录

        ```go
        // 获取最后一条记录（主键降序）
        db.Last(&user)
        // SELECT * FROM users ORDER BY id DESC LIMIT 1;
        ```

    - `First`，`Last`函数，仅在通过结构体和model值进行查询时才会生效，因为他需要使用结构体中的主键，或者是第一个字段来进行字段排序

        ```go
        var user User
        
        // 可以
        db.First(&user)
        // SELECT * FROM `users` ORDER BY `users`.`id` LIMIT 1
        
        // 可以
        result := map[string]interface{}{}
        db.Model(&User{}).First(&result)
        // SELECT * FROM `users` ORDER BY `users`.`id` LIMIT 1
        
        // 不行
        result := map[string]interface{}{}
        db.Table("users").First(&result)
        
        // 但可以配合 Take 使用
        result := map[string]interface{}{}
        db.Table("users").Take(&result)
        
        // 根据第一个字段排序
        type Language struct {
          Code string
          Name string
        }
        db.First(&Language{})
        // SELECT * FROM `languages` ORDER BY `languages`.`code` LIMIT 1
        ```

    - 返回值，当成功时，返回找到的记录数，没有找到时，返回 `ErrRecordNotFound` 错误

        ```go
        result := db.First(&user)
        result.RowsAffected // 返回找到的记录数
        result.Error        // returns error
        
        // 检查 ErrRecordNotFound 错误
        errors.Is(result.Error, gorm.ErrRecordNotFound)
        ```

- 根据主键查询

    - **内联条件**检索

        ```go
        db.First(&user, 10)
        // SELECT * FROM users WHERE id = 10;
        
        db.First(&user, "10")
        // SELECT * FROM users WHERE id = 10;
        
        db.Find(&users, []int{1,2,3})
        // SELECT * FROM users WHERE id IN (1,2,3);
        ```

- 检索全部对象

    - `Find`

        ```go
        // 获取全部记录
        result := db.Find(&users)
        // SELECT * FROM users;
        
        result.RowsAffected // 返回找到的记录数，相当于 `len(users)`
        result.Error        // returns error
        ```

- 检索条件

    - `Where`函数，支持string类型的条件以及struct&Map类型的条件

        ```go
        // 获取第一条匹配的记录
        db.Where("name = ?", "jinzhu").First(&user)
        // SELECT * FROM users WHERE name = 'jinzhu' ORDER BY id LIMIT 1;
        
        // 获取全部匹配的记录
        db.Where("name <> ?", "jinzhu").Find(&users)
        // SELECT * FROM users WHERE name <> 'jinzhu';
        
        // IN
        db.Where("name IN ?", []string{"jinzhu", "jinzhu 2"}).Find(&users)
        // SELECT * FROM users WHERE name IN ('jinzhu','jinzhu 2');
        
        // LIKE
        db.Where("name LIKE ?", "%jin%").Find(&users)
        // SELECT * FROM users WHERE name LIKE '%jin%';
        
        // AND
        db.Where("name = ? AND age >= ?", "jinzhu", "22").Find(&users)
        // SELECT * FROM users WHERE name = 'jinzhu' AND age >= 22;
        
        // Time
        db.Where("updated_at > ?", lastWeek).Find(&users)
        // SELECT * FROM users WHERE updated_at > '2000-01-01 00:00:00';
        
        // BETWEEN
        db.Where("created_at BETWEEN ? AND ?", lastWeek, today).Find(&users)
        // SELECT * FROM users WHERE created_at BETWEEN '2000-01-01 00:00:00' AND '2000-01-08 00:00:00';
        ```

    - Not条件，使用`Not`函数

        ```go
        db.Not("name = ?", "jinzhu").First(&user)
        // SELECT * FROM users WHERE NOT name = "jinzhu" ORDER BY id LIMIT 1;
        
        // Not In
        db.Not(map[string]interface{}{"name": []string{"jinzhu", "jinzhu 2"}}).Find(&users)
        // SELECT * FROM users WHERE name NOT IN ("jinzhu", "jinzhu 2");
        
        // Struct
        db.Not(User{Name: "jinzhu", Age: 18}).First(&user)
        // SELECT * FROM users WHERE name <> "jinzhu" AND age <> 18 ORDER BY id LIMIT 1;
        
        // 不在主键切片中的记录
        db.Not([]int64{1,2,3}).First(&user)
        // SELECT * FROM users WHERE id NOT IN (1,2,3) ORDER BY id LIMIT 1;
        ```

    - Or条件，使用`Or`函数

        ```go
        Selectdb.Where("role = ?", "admin").Or("role = ?", "super_admin").Find(&users)
        // SELECT * FROM users WHERE role = 'admin' OR role = 'super_admin';
        
        // Struct
        db.Where("name = 'jinzhu'").Or(User{Name: "jinzhu 2", Age: 18}).Find(&users)
        // SELECT * FROM users WHERE name = 'jinzhu' OR (name = 'jinzhu 2' AND age = 18);
        
        // Map
        db.Where("name = 'jinzhu'").Or(map[string]interface{}{"name": "jinzhu 2", "age": 18}).Find(&users)
        // SELECT * FROM users WHERE name = 'jinzhu' OR (name = 'jinzhu 2' AND age = 18);
        ```
    
- Struct&Map条件
  
        ```go
        // Struct
        db.Where(&User{Name: "jinzhu", Age: 20}).First(&user)
        // SELECT * FROM users WHERE name = "jinzhu" AND age = 20 ORDER BY id LIMIT 1;
        
        // Map
        db.Where(map[string]interface{}{"name": "jinzhu", "age": 20}).Find(&users)
        // SELECT * FROM users WHERE name = "jinzhu" AND age = 20;
        
        // 主键切片条件
        db.Where([]int64{20, 21, 22}).Find(&users)
        // SELECT * FROM users WHERE id IN (20, 21, 22);
    ```
    
    - 在使用**结构体**查询时，GORM只会查询非零值字段，当查询字段值为 `0`、`''`、`false` 或其他 [零值](https://tour.golang.org/basics/12)，该字段不会被用于构建查询条件
    
            ```go
            db.Where(&User{Name: "jinzhu", Age: 0}).Find(&users)
            // SELECT * FROM users WHERE name = "jinzhu";
    ```
    
    - 可以**使用`map`来构建**该类零值查询条件
    
            ```go
            db.Where(map[string]interface{}{"Name": "jinzhu", "Age": 0}).Find(&users)
            // SELECT * FROM users WHERE name = "jinzhu" AND age = 0;
            ```
        
    - 内联条件,即`不使用Where`函数完成查询
    
            ```go
            // SELECT * FROM users WHERE id = 23;
            // 根据主键获取记录，如果是非整型主键
            db.First(&user, "id = ?", "string_primary_key")
            // SELECT * FROM users WHERE id = 'string_primary_key';
            
            // Plain SQL
            db.Find(&user, "name = ?", "jinzhu")
            // SELECT * FROM users WHERE name = "jinzhu";
            
            db.Find(&users, "name <> ? AND age > ?", "jinzhu", 20)
            // SELECT * FROM users WHERE name <> "jinzhu" AND age > 20;
            
            // Struct
            db.Find(&users, User{Age: 20})
            // SELECT * FROM users WHERE age = 20;
            
            // Map
            db.Find(&users, map[string]interface{}{"age": 20})
            // SELECT * FROM users WHERE age = 20;
            ```
    
- **字段选择**

    - Select，**选择特定字段**

        ```go
        db.Select("name", "age").Find(&users)
        // SELECT name, age FROM users;
        
        db.Select([]string{"name", "age"}).Find(&users)
        // SELECT name, age FROM users;
        
        db.Table("users").Select("COALESCE(age,?)", 42).Rows()
        // SELECT COALESCE(age,'42') FROM users;
        ```

    - **智能选择字段**，通过定义一个查询结构体，在调用时自动选择字段

        ```go
        type User struct {
          ID     uint
          Name   string
          Age    int
          Gender string
          // 假设后面还有几百个字段...
        }
        
        //查询字段的小结构体
        type APIUser struct {
          ID   uint
          Name string
        }
        
        // 查询时会自动选择 `id`, `name` 字段
        db.Model(&User{}).Limit(10).Find(&APIUser{})
        // SELECT `id`, `name` FROM `users` LIMIT 10
        ```

- **Order**，指定数据库检索记录时的排序方式

    ```go
    db.Order("age desc, name").Find(&users)
    // SELECT * FROM users ORDER BY age desc, name;
    
    // 多个 order
    db.Order("age desc").Order("name").Find(&users)
    // SELECT * FROM users ORDER BY age desc, name;
    
    db.Clauses(clause.OrderBy{
      Expression: clause.Expr{SQL: "FIELD(id,?)", Vars: []interface{}{[]int{1, 2, 3}}, WithoutParentheses: true},
    }).Find(&User{})
    // SELECT * FROM users ORDER BY FIELD(id,1,2,3)
    ```

    - `Order`就是`order by`语句，所以当`Order`函数后接`First`函数或者`Last`时，`First`和`Last`的order将会失效

- **Limit & Offset**函数，并且可以通过传值为`-1`重置这些条件

    ```go
    db.Limit(3).Find(&users)
    // SELECT * FROM users LIMIT 3;
    
    // 通过 -1 消除 Limit 条件
    db.Limit(10).Find(&users1).Limit(-1).Find(&users2)
    // SELECT * FROM users LIMIT 10; (users1)
    // SELECT * FROM users; (users2)
    
    db.Offset(3).Find(&users)
    // SELECT * FROM users OFFSET 3;
    
    db.Limit(10).Offset(5).Find(&users)
    // SELECT * FROM users OFFSET 5 LIMIT 10;
    
    // 通过 -1 消除 Offset 条件
    db.Offset(10).Find(&users1).Offset(-1).Find(&users2)
    // SELECT * FROM users OFFSET 10; (users1)
    // SELECT * FROM users; (users2)
    ```

    - 分页查询器

        ```go
        func Paginate(r *http.Request) func(db *gorm.DB) *gorm.DB {
          return func (db *gorm.DB) *gorm.DB {
            //此处应该传入page_num,page_size,而不是使用*http.Request类型
            page, _ := strconv.Atoi(r.Query("page"))
            if page == 0 {
              page = 1
            }
        
            pageSize, _ := strconv.Atoi(r.Query("page_size"))
            switch {
            case pageSize > 100:
              pageSize = 100
            case pageSize <= 0:
              pageSize = 10
            }
        
            offset := (page - 1) * pageSize
            return db.Offset(offset).Limit(pageSize)
          }
        }
        
        db.Scopes(Paginate(r)).Find(&users)
        db.Scopes(Paginate(r)).Find(&articles)
        ```

- **Group  & Having**

    ```go
    type result struct {
      Date  time.Time
      Total int
    }
    
    db.Model(&User{}).Select("name, sum(age) as total").Where("name LIKE ?", "group%").Group("name").First(&result)
    // SELECT name, sum(age) as total FROM `users` WHERE name LIKE "group%" GROUP BY `name`
    
    db.Model(&User{}).Select("name, sum(age) as total").Group("name").Having("name = ?", "group").Find(&result)
    // SELECT name, sum(age) as total FROM `users` GROUP BY `name` HAVING name = "group
    ```

- **Distinct**，从模型中选择不想同的值

    ```go
    db.Distinct("name", "age").Order("name, age desc").Find(&results)
    ```

- **Joins**，感觉像脱裤子放屁，都写到这个份上了，还不如直接写SQL

    ```go
    type result struct {
      Name  string
      Email string
    }
    db.Model(&User{}).Select("users.name, emails.email").Joins("left join emails on emails.user_id = users.id").Scan(&result{})
    // SELECT users.name, emails.email FROM `users` left join emails on emails.user_id = users.id
    
    rows, err := db.Table("users").Select("users.name, emails.email").Joins("left join emails on emails.user_id = users.id").Rows()
    for rows.Next() {
      ...
    }
    
    db.Table("users").Select("users.name, emails.email").Joins("left join emails on emails.user_id = users.id").Scan(&results)
    
    // 带参数的多表连接
    db.Joins("JOIN emails ON emails.user_id = users.id AND emails.email = ?", "jinzhu@example.org").Joins("JOIN credit_cards ON credit_cards.user_id = users.id").Where("credit_cards.number = ?", "411111111111").Find(&user)
    ```

    - Joins预加载，`Joins Predlaod`会使用inner join加载相关数据

        ```go
        db.Joins("Company").Joins("Manager").Joins("Account").First(&user, 1)
        db.Joins("Company").Joins("Manager").Joins("Account").First(&user, "users.name = ?", "jinzhu")
        db.Joins("Company").Joins("Manager").Joins("Account").Find(&users, "users.id IN ?", []int{1,2,3,4,5})
        ```

- **Count**，用于获取匹配的记录数

    ```go
    var count int64
    db.Model(&User{}).Where("name = ?", "jinzhu").Or("name = ?", "jinzhu 2").Count(&count)
    // SELECT count(1) FROM users WHERE name = 'jinzhu' OR name = 'jinzhu 2'
    
    db.Model(&User{}).Where("name = ?", "jinzhu").Count(&count)
    // SELECT count(1) FROM users WHERE name = 'jinzhu'; (count)
    
    db.Table("deleted_users").Count(&count)
    // SELECT count(1) FROM deleted_users;
    ```

    

- **Scan**，扫描结果到结构体中，用法和Find类似

    ```go
    type Result struct {
      Name string
      Age  int
    }
    
    var result Result
    db.Table("users").Select("name", "age").Where("name = ?", "Antonio").Scan(&result)
    
    // 使用原生SQL时，利用Scan扫描数据
    db.Raw("SELECT name, age FROM users WHERE name = ?", "Antonio").Scan(&result)
    ```

- **Rows**，支持通过行进行迭代

    ```go
    rows, err := db.Model(&User{}).Where("name = ?", "jinzhu").Rows()
    defer rows.Close()
    
    for rows.Next() {
      var user User
      // ScanRows 方法用于将一行记录扫描至结构体
      db.ScanRows(rows, &user)
    }
    ```

    

- 命名参数，通过

- 可嵌套的子查询，查询语句可以嵌套，形成子查询

    ```go
    db.Where("amount > (?)", db.Table("orders").Select("AVG(amount)")).Find(&orders)
    // SELECT * FROM "orders" WHERE amount > (SELECT AVG(amount) FROM "orders");
    
    subQuery := db.Select("AVG(age)").Where("name LIKE ?", "name%").Table("users")
    db.Select("AVG(age) as avgage").Group("name").Having("AVG(age) > (?)", subQuery).Find(&results)
    // SELECT AVG(age) as avgage FROM `users` GROUP BY `name` HAVING AVG(age) > (SELECT AVG(age) FROM `users` WHERE name LIKE "name%")
    ```

    - 将嵌套的条件，Group可以实现很复杂的SQL，但是为什么不直接使用原生SQL呢？

        ```go
        db.Where(
            db.Where("pizza = ?", "pepperoni").Where(db.Where("size = ?", "small").Or("size = ?", "medium")),
        ).Or(
            db.Where("pizza = ?", "hawaiian").Where("size = ?", "xlarge"),
        ).Find(&Pizza{}).Statement
        
        // SELECT * FROM `pizzas` WHERE (pizza = "pepperoni" AND (size = "small" OR size = "medium")) OR (pizza = "hawaiian" AND size = "xlarge")
        ```

        

- **From**子查询,允许在`Table`方法中嵌套一条新的查询语句

    ```go
    db.Table("(?) as u", db.Model(&User{}).Select("name", "age")).Where("age = ?", 18}).Find(&User{})
    // SELECT * FROM (SELECT `name`,`age` FROM `users`) as u WHERE `age` = 18
    
    subQuery1 := db.Model(&User{}).Select("name")
    subQuery2 := db.Model(&Pet{}).Select("name")
    db.Table("(?) as u, (?) as p", subQuery1, subQuery2).Find(&User{})
    // SELECT * FROM (SELECT `name` FROM `users`) as u, (SELECT `name` FROM `pets`) as p
    ```

- **Find**至map，通过指定 `Model` 或 `Table`，扫描至 `map[string]interface{}` 或 `[]map[string]interface{}`

    ```go
    var result map[string]interface{}
    db.Model(&User{}).First(&result, "id = ?", 1)
    
    var results []map[string]interface{}
    db.Table("users").Find(&results)
    ```

- Pluck，将单列数据，查询后返回到切片中

    ```go
    var ages []int64
    db.Model(&users).Pluck("age", &ages)
    
    var names []string
    db.Model(&User{}).Pluck("name", &names)
    
    db.Table("deleted_users").Pluck("name", &names)
    
    // Distinct Pluck
    db.Model(&User{}).Distinct().Pluck("Name", &names)
    // SELECT DISTINCT `name` FROM `users`
    ```

    

- Scopes，通过将常用的查询，实现为一种接口，就可以在Scopes中进行调用，方便查询

    ```go
    func AmountGreaterThan1000(db *gorm.DB) *gorm.DB {
      return db.Where("amount > ?", 1000)
    }
    
    func PaidWithCreditCard(db *gorm.DB) *gorm.DB {
      return db.Where("pay_mode_sign = ?", "C")
    }
    
    func PaidWithCod(db *gorm.DB) *gorm.DB {
      return db.Where("pay_mode_sign = ?", "C")
    }
    
    func OrderStatus(status []string) func (db *gorm.DB) *gorm.DB {
      return func (db *gorm.DB) *gorm.DB {
        return db.Where("status IN (?)", status)
      }
    }
    
    db.Scopes(AmountGreaterThan1000, PaidWithCreditCard).Find(&orders)
    // 查找所有金额大于 1000 的信用卡订单
    
    db.Scopes(AmountGreaterThan1000, PaidWithCod).Find(&orders)
    // 查找所有金额大于 1000 的货到付款订单
    
    db.Scopes(AmountGreaterThan1000, OrderStatus([]string{"paid", "shipped"})).Find(&orders)
    // 查找所有金额大于 1000 且已付款或已发货的订单
    ```

- 优化查询计划

    ```go
    import "gorm.io/hints"
    
    db.Clauses(hints.New("MAX_EXECUTION_TIME(10000)")).Find(&User{})
    // SELECT * /*+ MAX_EXECUTION_TIME(10000) */ FROM `users`
    ```

    

- 指定索引

    ```go
    import "gorm.io/hints"
    
    db.Clauses(hints.UseIndex("idx_user_name")).Find(&User{})
    // SELECT * FROM `users` USE INDEX (`idx_user_name`)
    
    db.Clauses(hints.ForceIndex("idx_user_name", "idx_user_id").ForJoin()).Find(&User{})
    // SELECT * FROM `users` FORCE INDEX FOR JOIN (`idx_user_name`,`idx_user_id`)"
    ```

    

- Hook，查询操作，支持`AfterFind`hook，查询记录时会调用

    ```go
    func (u *User) AfterFind(tx *gorm.DB) (err error) {
      if u.Role == "" {
        u.Role = "user"
      }
      return
    }
    ```

- 查询控制，针对查询结果执行额外的任务[查询控制](https://learnku.com/docs/gorm/v2/advanced_query/9757#88c728)

- 原生SQL查询

    - `Raw`形式

        ```go
        type Result struct {
          ID   int
          Name string
          Age  int
        }
        
        var result Result
        db.Raw("SELECT id, name, age FROM users WHERE id = ?", 3).Scan(&result)
        
        var age int
        db.Raw("select sum(age) from users where role = ?", "admin").Scan(&age)
        ```

    - `Exec`函数

        ```go
        db.Exec("DROP TABLE users")
        db.Exec("UPDATE orders SET shipped_at=? WHERE id IN ?", time.Now(), []int64{1,2,3})
        
        // Exec SQL 表达式
        db.Exec("update users set money=? where name = ?", gorm.Expr("money * ? + ?", 10000, 1), "jinzhu")
        ```

    - 命名参数，支持在`Where`，`Raw`,`Exec`等函数中使用，效果同上

        ```go
        db.Where("name1 = @name OR name2 = @name", sql.Named("name", "jinzhu")).Find(&user)
        // SELECT * FROM `users` WHERE name1 = "jinzhu" OR name2 = "jinzhu"
        
        db.Where("name1 = @name OR name2 = @name", map[string]interface{}{"name": "jinzhu2"}).First(&result3)
        // SELECT * FROM `users` WHERE name1 = "jinzhu2" OR name2 = "jinzhu2" ORDER BY `users`.`id` LIMIT 1
        
        // 原生 SQL 及命名参数
        db.Raw("SELECT * FROM users WHERE name1 = @name OR name2 = @name2 OR name3 = @name",
           sql.Named("name", "jinzhu1"), sql.Named("name2", "jinzhu2")).Find(&user)
        // SELECT * FROM users WHERE name1 = "jinzhu1" OR name2 = "jinzhu2" OR name3 = "jinzhu1"
        
        db.Exec("UPDATE users SET name1 = @name, name2 = @name2, name3 = @name",
           sql.Named("name", "jinzhunew"), sql.Named("name2", "jinzhunew2"))
        // UPDATE users SET name1 = "jinzhunew", name2 = "jinzhunew2", name3 = "jinzhunew"
        
        db.Raw("SELECT * FROM users WHERE (name1 = @name AND name3 = @name) AND name2 = @name2",
           map[string]interface{}{"name": "jinzhu", "name2": "jinzhu2"}).Find(&user)
        // SELECT * FROM users WHERE (name1 = "jinzhu" AND name3 = "jinzhu") AND name2 = "jinzhu2"
        
        type NamedArgument struct {
            Name string
            Name2 string
        }
        
        db.Raw("SELECT * FROM users WHERE (name1 = @Name AND name3 = @Name) AND name2 = @Name2",
             NamedArgument{Name: "jinzhu", Name2: "jinzhu2"}).Find(&user)
        // SELECT * FROM users WHERE (name1 = "jinzhu" AND name3 = "jinzhu") AND name2 = "jinzhu2"
        ```

        

##### 更新

- `Save`,**保存所有字段**，即使字段是零值

    ```go
    db.First(&user)
    
    user.Name = "jinzhu 2"
    user.Age = 100
    db.Save(&user)
    // UPDATE users SET name='jinzhu 2', age=100, birthday='2016-01-01', updated_at = '2013-11-17 21:34:10' WHERE id=111;
    ```

- 使用`Select`,`Omit`函数，在`struct`或者`map[string]interface{}`**更新选定字段**

    ```go
    // Select 和 Map
    // User's ID is `111`:
    db.Model(&user).Select("name").Updates(map[string]interface{}{"name": "hello", "age": 18, "actived": false})
    // UPDATE users SET name='hello' WHERE id=111;
    
    db.Model(&user).Omit("name").Updates(map[string]interface{}{"name": "hello", "age": 18, "actived": false})
    // UPDATE users SET age=18, actived=false, updated_at='2013-11-17 21:34:10' WHERE id=111;
    
    // Select 和 Struct （可以选中更新零值字段）
    db.Model(&result).Select("Name", "Age").Updates(User{Name: "new_name", Age: 0})
    // UPDATE users SET name='new_name', age=0 WHERE id=111;
    ```

    

- `Update`，更新单列

    ```go
    // 条件更新
    db.Model(&User{}).Where("active = ?", true).Update("name", "hello")
    // UPDATE users SET name='hello', updated_at='2013-11-17 21:34:10' WHERE active=true;
    
    // User 的 ID 是 `111`
    db.Model(&user).Update("name", "hello")
    // UPDATE users SET name='hello', updated_at='2013-11-17 21:34:10' WHERE id=111;
    
    // 根据条件和 model 的值进行更新
    db.Model(&user).Where("active = ?", true).Update("name", "hello")
    // UPDATE users SET name='hello', updated_at='2013-11-17 21:34:10' WHERE id=111 AND active=true;
    ```

    - 注意点：需要指定条件进行更新，否则会返回`ErrMissingWhereClause` 错误

- Updates，更新多列，支持struct和map[string]interface{} 作为参数

    ```go
    // 根据 `struct` 更新属性，只会更新非零值的字段
    db.Model(&user).Updates(User{Name: "hello", Age: 18, Active: false})
    // UPDATE users SET name='hello', age=18, updated_at = '2013-11-17 21:34:10' WHERE id = 111;
    
    // 根据 `map` 更新属性
    db.Model(&user).Updates(map[string]interface{}{"name": "hello", "age": 18, "actived": false})
    // UPDATE users SET name='hello', age=18, actived=false, updated_at='2013-11-17 21:34:10' WHERE id=111;
    ```

    - 获取受影响的行数，Updates返回更新的记录数和更新时发生的异常

        ```go
        // 通过 `RowsAffected` 得到更新的记录数
        result := db.Model(User{}).Where("role = ?", "admin").Updates(User{Name: "hello", Age: 18})
        // UPDATE users SET name='hello', age=18 WHERE role = 'admin;
        
        result.RowsAffected // 更新的记录数
        result.Error        // 更新的错误
        ```

        

- 批量更新，当数据对象`Model`中**没有指定主键**，那么就会更新条件中的全部记录

    ```go
    // 根据 struct 更新
    db.Model(User{}).Where("role = ?", "admin").Updates(User{Name: "hello", Age: 18})
    // UPDATE users SET name='hello', age=18 WHERE role = 'admin;
    
    // 根据 map 更新
    db.Table("users").Where("id IN ?", []int{10, 11}).Updates(map[string]interface{}{"name": "hello", "age": 18})
    // UPDATE users SET name='hello', age=18 WHERE id IN (10, 11);
    ```

- 强制全局更新，默认GORM不会执行为加条件的批量更新，因此需要使用原生SQL或者加一些额外的条件

    ```go
    db.Model(&User{}).Update("name", "jinzhu").Error // gorm.ErrMissingWhereClause
    
    db.Model(&User{}).Where("1 = 1").Update("name", "jinzhu")
    // UPDATE users SET `name` = "jinzhu" WHERE 1=1
    
    db.Exec("UPDATE users SET name = ?", "jinzhu")
    // UPDATE users SET name = "jinzhu"
    
    db.Session(&gorm.Session{AllowGlobalUpdate: true}).Model(&User{}).Update("name", "jinzhu")
    // UPDATE users SET `name` = "jinzhu"
    ```

- 使用SQL表达式和` Context Valuer `更新列

    - SQL表达式

        ```go
        // product 的 ID 是 `3`
        db.Model(&product).Update("price", gorm.Expr("price * ? + ?", 2, 100))
        // UPDATE "products" SET "price" = price * 2 + 100, "updated_at" = '2013-11-17 21:34:10' WHERE "id" = 3;
        
        db.Model(&product).Updates(map[string]interface{}{"price": gorm.Expr("price * ? + ?", 2, 100)})
        // UPDATE "products" SET "price" = price * 2 + 100, "updated_at" = '2013-11-17 21:34:10' WHERE "id" = 3;
        
        db.Model(&product).UpdateColumn("quantity", gorm.Expr("quantity - ?", 1))
        // UPDATE "products" SET "quantity" = quantity - 1 WHERE "id" = 3;
        
        db.Model(&product).Where("quantity > 1").UpdateColumn("quantity", gorm.Expr("quantity - ?", 1))
        // UPDATE "products" SET "quantity" = quantity - 1 WHERE "id" = 3 AND quantity > 1;
        ```

    - `Context Valuer`

        ```go
        // 根据自定义数据类型创建
        type Location struct {
            X, Y int
        }
        
        func (loc Location) GormValue(ctx context.Context, db *gorm.DB) clause.Expr {
          return clause.Expr{
            SQL:  "ST_PointFromText(?)",
            Vars: []interface{}{fmt.Sprintf("POINT(%d %d)", loc.X, loc.Y)},
          }
        }
        
        db.Model(&User{ID: 1}).Updates(User{
          Name:  "jinzhu",
          Point: Point{X: 100, Y: 100},
        })
        // UPDATE `user_with_points` SET `name`="jinzhu",`point`=ST_PointFromText("POINT(100 100)") WHERE `id` = 1
        ```

        

- Hook

    ```go
    // 开始事务
    BeforeSave
    BeforeUpdate
    // 关联前的 save
    // 更新 db
    // 关联后的 save
    AfterUpdate
    AfterSave
    // 提交或回滚事务
    ```

    - 示例

        ```go
        func (u *User) BeforeUpdate(tx *gorm.DB) (err error) {
          if u.readonly() {
            err = errors.New("read only user")
          }
          return
        }
        
        // 在同一个事务中更新数据
        func (u *User) AfterUpdate(tx *gorm.DB) (err error) {
          if u.Confirmed {
            tx.Model(&Address{}).Where("user_id = ?", u.ID).Update("verfied", true)
          }
          return
        }
        ```

- `UpdateColumn`，`UpdateColumns`**跳过Hook**，并且不自动追踪更新时间

    ```go
    // 更新单个列
    db.Model(&user).UpdateColumn("name", "hello")
    // UPDATE users SET name='hello' WHERE id = 111;
    
    // 更新多个列
    db.Model(&user).UpdateColumns(User{Name: "hello", Age: 18})
    // UPDATE users SET name='hello', age=18 WHERE id = 111;
    
    // 更新选中的列
    db.Model(&user).Select("name", "age").UpdateColumns(User{Name: "hello", Age: 0})
    // UPDATE users SET name='hello', age=0 WHERE id = 111;
    ```

- `Changed`检查Model对象字段是否与`Update`，`Updates`的值是否一样，**字段是否有变更**，当字段未被忽略，且发生变更，则返回true，可以用在`Before Update Hook`

    - 注意：`Changed`方法只能与`Update`，`Updates`一起使用

    ```go
    func (u *User) BeforeUpdate(tx *gorm.DB) (err error) {
      // 如果 Role 字段有变更
        if tx.Statement.Changed("Role") {
        return errors.New("role not allowed to change")
        }
    
      if tx.Statement.Changed("Name", "Admin") { // 如果 Name 或 Role 字段有变更
        tx.Statement.SetColumn("Age", 18)
      }
    
      // 如果任意字段有变更
        if tx.Statement.Changed() {
            tx.Statement.SetColumn("RefreshedAt", time.Now())
        }
        return nil
    }
    
    db.Model(&User{ID: 1, Name: "jinzhu"}).Updates(map[string]interface{"name": "jinzhu2"})
    // Changed("Name") => true
    db.Model(&User{ID: 1, Name: "jinzhu"}).Updates(map[string]interface{"name": "jinzhu"})
    // Changed("Name") => false, 因为 `Name` 没有变更
    db.Model(&User{ID: 1, Name: "jinzhu"}).Select("Admin").Updates(map[string]interface{
      "name": "jinzhu2", "admin": false,
    })
    // Changed("Name") => false, 因为 `Name` 没有被 Select 选中并更新
    
    db.Model(&User{ID: 1, Name: "jinzhu"}).Updates(User{Name: "jinzhu2"})
    // Changed("Name") => true
    db.Model(&User{ID: 1, Name: "jinzhu"}).Updates(User{Name: "jinzhu"})
    // Changed("Name") => false, 因为 `Name` 没有变更
    db.Model(&User{ID: 1, Name: "jinzhu"}).Select("Admin").Updates(User{Name: "jinzhu2"})
    // Changed("Name") => false, 因为 `Name` 没有被 Select 选中并更新
    ```

- `SetColumn`更新时在Hook中**变更字段值**

    ```go
    func (user *User) BeforeSave(tx *gorm.DB) (err error) {
      if pw, err := bcrypt.GenerateFromPassword(user.Password, 0); err == nil {
        tx.Statement.SetColumn("EncryptedPassword", pw)
      }
    
      if tx.Statement.Changed("Code") {
        s.Age += 20
        tx.Statement.SetColumn("Age", s.Age+20)
      }
    }
    
    db.Model(&user).Update("Name", "jinzhu")
    ```

    

##### 删除

- `Delete`指定主键，删除一条记录

    ```go
    db.Delete(&User{}, 10)
    // DELETE FROM users WHERE id = 10;
    
    db.Delete(&User{}, "10")
    // DELETE FROM users WHERE id = 10;
    
    db.Delete(&users, []int{1,2,3})
    // DELETE FROM users WHERE id IN (1,2,3);
    ```

    

- `Delete`不指定主键批量删除

    ```go
    db.Where("email LIKE ?", "%jinzhu%").Delete(Email{})
    // DELETE from emails where email LIKE "%jinzhu%";
    
    db.Delete(Email{}, "email LIKE ?", "%jinzhu%")
    // DELETE from emails where email LIKE "%jinzhu%";
    ```

    

- Gorm默认**不执行无条件的批量删除**，需要添加额外的条件以强制批量删除

    ```go
    db.Delete(&User{}).Error // gorm.ErrMissingWhereClause
    ```

    

    - 使用原生SQL

        ```go
        db.Exec("DELETE FROM users")
        // DELETE FROM users
        ```

        

    - 添加额外的条件

        ```go
        db.Where("1 = 1").Delete(&User{})
        // DELETE FROM `users` WHERE 1=1
        ```

        

    - 启用`AllowGlobalUpdate`模式

        ```go
        db.Session(&gorm.Session{AllowGlobalUpdate: true}).Delete(&User{})
        // DELETE FROM users
        ```

        

- 添加`gorm.Deleteat`字段，启用GORM的软删除

    - 启用软删除时，当使用`Delete`时，记录不会从数据库中删除，GORM会将`DeleteAt`置为当前时间，并且无法通过正常的查询方法找到该条记录

        ```go
        // user 的 ID 是 `111`
        db.Delete(&user)
        // UPDATE users SET deleted_at="2013-10-29 10:23" WHERE id = 111;
        
        // 批量删除
        db.Where("age = ?", 20).Delete(&User{})
        // UPDATE users SET deleted_at="2013-10-29 10:23" WHERE age = 20;
        ```

    - 正常查询无法找到被软删除的记录

        ```go
        // 在查询时会忽略被软删除的记录
        db.Where("age = 20").Find(&user)
        // SELECT * FROM users WHERE age = 20 AND deleted_at IS NULL;
        ```

        

    - 查找被软删除的记录

        ```go
        db.Unscoped().Where("age = 20").Find(&users)
        // SELECT * FROM users WHERE age = 20;
        ```

    - 永久删除

        ```go
        db.Unscoped().Delete(&order)
        // DELETE FROM orders WHERE id=10;
        ```

        

- Hook

    ```go
    // 开始事务
    BeforeDelete
    // 删除 db 中的数据
    AfterDelete
    // 提交或回滚事务
    ```

    - 示例

        ```go
        // 在同一个事务中更新数据
        func (u *User) AfterDelete(tx *gorm.DB) (err error) {
          if u.Confirmed {
            tx.Model(&Address{}).Where("user_id = ?", u.ID).Update("invalid", false)
          }
          return
        }
        ```

        

### Locking

- `FOR UPDATE`

    ```go
    db.Clauses(clause.Locking{Strength: "UPDATE"}).Find(&users)
    // SELECT * FROM `users` FOR UPDATE
    ```

- `FOR SHARE`

    ```go
    db.Clauses(clause.Locking{
      Strength: "SHARE",
      Table: clause.Table{Name: clause.CurrentTable},
    }).Find(&users)
    // SELECT * FROM `users` FOR SHARE OF `users`
    ```


### 关联

- Belongs To
- 