"""
图书馆管理系统
实现功能：
1. 书籍类：包含书名、作者、ISBN等属性
2. 用户类：包含姓名、借书卡号等属性
3. 图书馆类：管理所有书籍和用户
4. 实现借书、还书功能
5. 检查某本书是否可借
"""

class Book:
    """
    书籍类
    属性：书名、作者、ISBN、是否被借出
    """
    def __init__(self, title, author, isbn):
        self.title = title          # 书名
        self.author = author         # 作者
        self.isbn = isbn            # ISBN号（唯一标识）
        self.is_borrowed = False    # 是否被借出，默认为False
        self.borrower = None        # 当前借阅者（用户对象）
    
    def borrow(self, user):
        """
        借书方法
        参数：user - 借书的用户对象
        返回：成功返回True，失败返回False
        """
        if not self.is_borrowed:
            self.is_borrowed = True
            self.borrower = user
            return True
        return False
    
    def return_book(self):
        """
        还书方法
        返回：成功返回True，失败返回False
        """
        if self.is_borrowed:
            self.is_borrowed = False
            self.borrower = None
            return True
        return False
    
    def is_available(self):
        """
        检查书籍是否可借
        返回：可借返回True，不可借返回False
        """
        return not self.is_borrowed
    
    def get_status(self):
        """
        获取书籍状态信息
        返回：包含书籍详细信息的字典
        """
        status = "可借阅" if not self.is_borrowed else "已借出"
        borrower_name = self.borrower.name if self.borrower else "无"
        
        return {
            'title': self.title,
            'author': self.author,
            'isbn': self.isbn,
            'status': status,
            'borrower': borrower_name
        }
    
    def __str__(self):
        """字符串表示，便于打印"""
        status = "可借阅" if not self.is_borrowed else "已借出"
        return f"《{self.title}》- {self.author} (ISBN: {self.isbn}) - 状态: {status}"


class User:
    """
    用户类
    属性：姓名、借书卡号、已借书籍列表
    """
    def __init__(self, name, card_id):
        self.name = name                    # 姓名
        self.card_id = card_id              # 借书卡号（唯一标识）
        self.borrowed_books = []           # 已借书籍列表（存储Book对象）
        self.max_borrow_limit = 5          # 最大借书数量限制
    
    def can_borrow_more(self):
        """
        检查用户是否可以继续借书
        返回：可以返回True，不可以返回False
        """
        return len(self.borrowed_books) < self.max_borrow_limit
    
    def borrow_book(self, book):
        """
        用户借书
        参数：book - 要借的书籍对象
        返回：成功返回True，失败返回False
        """
        if not self.can_borrow_more():
            print(f"{self.name} 已达到最大借书数量限制（{self.max_borrow_limit}本）")
            return False
        
        if book.borrow(self):
            self.borrowed_books.append(book)
            print(f"{self.name} 成功借阅《{book.title}》")
            return True
        else:
            print(f"《{book.title}》已被借出，无法借阅")
            return False
    
    def return_book(self, book):
        """
        用户还书
        参数：book - 要还的书籍对象
        返回：成功返回True，失败返回False
        """
        if book in self.borrowed_books:
            if book.return_book():
                self.borrowed_books.remove(book)
                print(f"{self.name} 成功归还《{book.title}》")
                return True
        else:
            print(f"{self.name} 并未借阅《{book.title}》，无法归还")
            return False
    
    def show_borrowed_books(self):
        """
        显示用户当前借阅的所有书籍
        """
        if not self.borrowed_books:
            print(f"{self.name} 当前没有借阅任何书籍")
        else:
            print(f"{self.name} 当前借阅的书籍（共{len(self.borrowed_books)}本）：")
            for i, book in enumerate(self.borrowed_books, 1):
                print(f"  {i}. 《{book.title}》, 作者：{book.author}, ISBN：{book.isbn}")
    
    def __str__(self):
        """字符串表示，便于打印"""
        return f"用户: {self.name} (卡号: {self.card_id}) - 已借书籍: {len(self.borrowed_books)}本"


class Library:
    """
    图书馆类
    管理所有书籍和用户，提供借书、还书、查询等功能
    """
    def __init__(self, name):
        self.name = name                    # 图书馆名称
        self.books = {}                    # 书籍字典，key为ISBN，value为Book对象
        self.users = {}                    # 用户字典，key为卡号，value为User对象
        self.borrow_records = []          # 借阅记录列表
    
    def add_book(self, title, author, isbn):
        """
        添加新书到图书馆
        参数：title-书名, author-作者, isbn-ISBN号
        返回：成功返回True，失败返回False
        """
        if isbn in self.books:
            print(f"ISBN为 {isbn} 的书籍已存在，无法重复添加")
            return False
        
        book = Book(title, author, isbn)
        self.books[isbn] = book
        print(f"成功添加书籍: 《{title}》")
        return True
    
    def remove_book(self, isbn):
        """
        从图书馆移除书籍
        参数：isbn-ISBN号
        返回：成功返回True，失败返回False
        """
        if isbn not in self.books:
            print(f"ISBN为 {isbn} 的书籍不存在")
            return False
        
        book = self.books[isbn]
        if book.is_borrowed:
            print(f"《{book.title}》已被借出，无法移除")
            return False
        
        del self.books[isbn]
        print(f"成功移除书籍: 《{book.title}》")
        return True
    
    def register_user(self, name, card_id):
        """
        注册新用户
        参数：name-姓名, card_id-借书卡号
        返回：成功返回True，失败返回False
        """
        if card_id in self.users:
            print(f"卡号 {card_id} 已被注册")
            return False
        
        user = User(name, card_id)
        self.users[card_id] = user
        print(f"成功注册用户: {name} (卡号: {card_id})")
        return True
    
    def borrow_book(self, user_card_id, book_isbn):
        """
        借书功能
        参数：user_card_id-用户卡号, book_isbn-书籍ISBN
        返回：成功返回True，失败返回False
        """
        # 检查用户是否存在
        if user_card_id not in self.users:
            print(f"用户卡号 {user_card_id} 不存在")
            return False
        
        # 检查书籍是否存在
        if book_isbn not in self.books:
            print(f"ISBN为 {book_isbn} 的书籍不存在")
            return False
        
        user = self.users[user_card_id]
        book = self.books[book_isbn]
        
        # 执行借书操作
        if user.borrow_book(book):
            # 记录借阅信息
            record = {
                'user_name': user.name,
                'user_card_id': user_card_id,
                'book_title': book.title,
                'book_isbn': book_isbn,
                'borrow_time': "当前时间"  # 实际应用中可以使用datetime模块记录具体时间
            }
            self.borrow_records.append(record)
            return True
        
        return False
    
    def return_book(self, user_card_id, book_isbn):
        """
        还书功能
        参数：user_card_id-用户卡号, book_isbn-书籍ISBN
        返回：成功返回True，失败返回False
        """
        # 检查用户是否存在
        if user_card_id not in self.users:
            print(f"用户卡号 {user_card_id} 不存在")
            return False
        
        # 检查书籍是否存在
        if book_isbn not in self.books:
            print(f"ISBN为 {book_isbn} 的书籍不存在")
            return False
        
        user = self.users[user_card_id]
        book = self.books[book_isbn]
        
        # 执行还书操作
        return user.return_book(book)
    
    def check_book_availability(self, book_isbn):
        """
        检查某本书是否可借
        参数：book_isbn-书籍ISBN
        返回：可借返回True，不可借返回False，书籍不存在返回None
        """
        if book_isbn not in self.books:
            print(f"ISBN为 {book_isbn} 的书籍不存在")
            return None
        
        book = self.books[book_isbn]
        is_available = book.is_available()
        
        if is_available:
            print(f"《{book.title}》当前可借阅")
        else:
            print(f"《{book.title}》当前已被借出，借阅者：{book.borrower.name if book.borrower else '未知'}")
        
        return is_available
    
    def search_book(self, keyword):
        """
        搜索书籍
        参数：keyword-搜索关键词（书名、作者或ISBN）
        返回：匹配的书籍列表
        """
        results = []
        keyword = keyword.lower()
        
        for isbn, book in self.books.items():
            if (keyword in book.title.lower() or 
                keyword in book.author.lower() or 
                keyword in isbn.lower()):
                results.append(book)
        
        return results
    
    def display_all_books(self):
        """
        显示图书馆所有书籍
        """
        if not self.books:
            print(f"{self.name} 图书馆暂无藏书")
            return
        
        print(f"\n=== {self.name} 图书馆藏书列表 ===")
        print(f"共 {len(self.books)} 本书籍")
        print("-" * 80)
        
        for i, (isbn, book) in enumerate(self.books.items(), 1):
            status = "可借阅" if not book.is_borrowed else "已借出"
            borrower_info = f" (借阅者: {book.borrower.name})" if book.borrower else ""
            print(f"{i:3d}. 《{book.title:<20}》- {book.author:<15} (ISBN: {isbn:<13}) - 状态: {status:<6}{borrower_info}")
    
    def display_all_users(self):
        """
        显示所有注册用户
        """
        if not self.users:
            print("暂无注册用户")
            return
        
        print(f"\n=== 注册用户列表 ===")
        print(f"共 {len(self.users)} 位用户")
        print("-" * 60)
        
        for i, (card_id, user) in enumerate(self.users.items(), 1):
            print(f"{i:3d}. {user.name:<15} (卡号: {card_id:<10}) - 已借书籍: {len(user.borrowed_books)}本")
    
    def display_borrow_records(self):
        """
        显示借阅记录
        """
        if not self.borrow_records:
            print("暂无借阅记录")
            return
        
        print(f"\n=== 借阅记录 ===")
        print(f"共 {len(self.borrow_records)} 条记录")
        print("-" * 80)
        
        for i, record in enumerate(self.borrow_records, 1):
            print(f"{i:3d}. {record['user_name']} (卡号: {record['user_card_id']}) "
                  f"借阅了《{record['book_title']}》 (ISBN: {record['book_isbn']}) "
                  f"于 {record['borrow_time']}")


# 测试函数
def test_library_system():
    """
    测试图书馆系统功能
    """
    print("=" * 60)
    print("          图书馆管理系统测试")
    print("=" * 60)
    
    # 创建图书馆
    library = Library("中央图书馆")
    print(f"创建图书馆: {library.name}")
    
    # 添加书籍
    print("\n1. 添加书籍:")
    library.add_book("Python编程从入门到实践", "Eric Matthes", "9787115428028")
    library.add_book("流畅的Python", "Luciano Ramalho", "9787115454157")
    library.add_book("算法导论", "Thomas H. Cormen", "9787111407010")
    library.add_book("深入理解计算机系统", "Randal E. Bryant", "9787111544937")
    
    # 注册用户
    print("\n2. 注册用户:")
    library.register_user("张三", "2023001")
    library.register_user("李四", "2023002")
    library.register_user("王五", "2023003")
    
    # 显示所有书籍
    print("\n3. 显示所有书籍:")
    library.display_all_books()
    
    # 显示所有用户
    print("\n4. 显示所有用户:")
    library.display_all_users()
    
    # 测试借书功能
    print("\n5. 测试借书功能:")
    # 张三借阅Python编程从入门到实践
    library.borrow_book("2023001", "9787115428028")
    # 李四借阅同一本书（应该失败）
    library.borrow_book("2023002", "9787115428028")
    # 李四借阅另一本书
    library.borrow_book("2023002", "9787115454157")
    
    # 检查书籍是否可借
    print("\n6. 检查书籍是否可借:")
    library.check_book_availability("9787115428028")  # 应该显示不可借
    library.check_book_availability("9787111407010")  # 应该显示可借
    
    # 显示当前状态
    print("\n7. 当前状态:")
    library.display_all_books()
    
    # 测试还书功能
    print("\n8. 测试还书功能:")
    library.return_book("2023001", "9787115428028")
    
    # 再次检查书籍状态
    print("\n9. 再次检查书籍状态:")
    library.check_book_availability("9787115428028")
    
    # 显示最终状态
    print("\n10. 最终状态:")
    library.display_all_books()
    
    # 显示用户借阅情况
    print("\n11. 用户借阅情况:")
    for user in library.users.values():
        user.show_borrowed_books()
    
    # 显示借阅记录
    print("\n12. 借阅记录:")
    library.display_borrow_records()
    
    print("\n" + "=" * 60)
    print("          测试完成")
    print("=" * 60)


# 交互式菜单系统
def interactive_menu():
    """
    交互式菜单系统
    """
    library = Library("我的图书馆")
    
    # 初始化一些示例数据
    library.add_book("Python编程从入门到实践", "Eric Matthes", "9787115428028")
    library.add_book("流畅的Python", "Luciano Ramalho", "9787115454157")
    library.add_book("算法导论", "Thomas H. Cormen", "9787111407010")
    library.register_user("张三", "001")
    library.register_user("李四", "002")
    
    while True:
        print("\n" + "=" * 60)
        print("          图书馆管理系统")
        print("=" * 60)
        print("1. 浏览所有书籍")
        print("2. 搜索书籍")
        print("3. 添加新书")
        print("4. 注册新用户")
        print("5. 借书")
        print("6. 还书")
        print("7. 检查书籍是否可借")
        print("8. 查看用户借阅情况")
        print("9. 查看所有用户")
        print("10. 查看借阅记录")
        print("0. 退出系统")
        print("=" * 60)
        
        choice = input("请选择操作 (0-10): ").strip()
        
        if choice == '0':
            print("感谢使用图书馆管理系统，再见！")
            break
        
        elif choice == '1':
            library.display_all_books()
        
        elif choice == '2':
            keyword = input("请输入搜索关键词（书名/作者/ISBN）: ").strip()
            results = library.search_book(keyword)
            if results:
                print(f"\n找到 {len(results)} 本相关书籍:")
                for i, book in enumerate(results, 1):
                    print(f"{i}. {book}")
            else:
                print("未找到相关书籍")
        
        elif choice == '3':
            title = input("请输入书名: ").strip()
            author = input("请输入作者: ").strip()
            isbn = input("请输入ISBN: ").strip()
            library.add_book(title, author, isbn)
        
        elif choice == '4':
            name = input("请输入姓名: ").strip()
            card_id = input("请输入借书卡号: ").strip()
            library.register_user(name, card_id)
        
        elif choice == '5':
            library.display_all_books()
            book_isbn = input("请输入要借阅书籍的ISBN: ").strip()
            user_card_id = input("请输入您的借书卡号: ").strip()
            library.borrow_book(user_card_id, book_isbn)
        
        elif choice == '6':
            user_card_id = input("请输入您的借书卡号: ").strip()
            book_isbn = input("请输入要归还书籍的ISBN: ").strip()
            library.return_book(user_card_id, book_isbn)
        
        elif choice == '7':
            book_isbn = input("请输入要检查的书籍ISBN: ").strip()
            library.check_book_availability(book_isbn)
        
        elif choice == '8':
            user_card_id = input("请输入用户卡号: ").strip()
            if user_card_id in library.users:
                library.users[user_card_id].show_borrowed_books()
            else:
                print("用户不存在")
        
        elif choice == '9':
            library.display_all_users()
        
        elif choice == '10':
            library.display_borrow_records()
        
        else:
            print("无效的选择，请重新输入！")


# 主程序入口
if __name__ == "__main__":
    print("=" * 60)
    print("          图书馆管理系统")
    print("=" * 60)
    print("请选择运行模式:")
    print("1. 运行测试程序")
    print("2. 运行交互式菜单")
    print("=" * 60)
    
    mode = input("请选择模式 (1或2): ").strip()
    
    if mode == '1':
        test_library_system()
    elif mode == '2':
        interactive_menu()
    else:
        print("无效的选择，默认运行测试程序")
        test_library_system()

