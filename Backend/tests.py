from repository.user_repository import UserRepository
from repository.utils import hash_password, verify_password

def main():
  ""Проверка правильности работы функций""
  repo = UserRepository()

  email = "user@example.com"
  password = "securepassword"
  hashed = hash_password(password)
  
  user = None
  fetched_user = None
  updated_user = None
  
""Проверка на создание пользователя и дальнейшее его отображение в таблице""
  try:
    user = repo.create_user(email, hashed)
    fetched_user = repo.get_user_by_email(email)
    all_users = repo.get_all_users()
    if user in all_users: print('1/6 тестов пройдены успешно")
    else:
      print("Пользователь не отображается в общем списке пользователей")
      return False
  except Exception as e:
    print(f'Не удалось выполнить необходимые требования, ошибка: {e}')
    return False

  ""Проверка на вход по паролю""
  try:
  
    ""Проверка работы при введении верного пороля""
    check = verify_password("securepassword", fetched_user.hashed_password)
    if not(check): 
      print("При введении верного пароля не считает его правильным")
      return False

    ""Проверка на введение неверного пароля""  
    check = verify_password("notsecurepassword", fetched_user.hashed_password)
    if check:
      print("При введении неверного пароля считает его верным")
      return False
      
    print("2/6 тестов пройдены успешно")
    
  except Exception as e:
    print(f'Возникла ошибка внутри функции проверки паролей, а не по результатам её работы. Ошибка: {e}')
    return False

  ""Проверка изменения пользователей""
  try:
    new_password = "newsecurepassword"
    new_hashed = hash_password(new_password)
    updated_user = repo.update_user(fetched_user.id, hashed_password=new_hashed)
    if updated_user:
        print("3/6 тестов пройдены успешно")
    else:
        print("Не удалось обновить пользователя по ID")
        return False
        
  except Exception as e:
    print(f'Возникла ошибка внутри функции обновления пользователей, а не по результатам её работы. Ошибка: {e}')
    return False

  ""Проверка изменений в пароле""
  try:
    
    ""Проверка работы при введении верного пороля""
    check = verify_password("newsecurepassword", fetched_user.hashed_password)
    if not(check): 
      print("При введении верного пароля не считает его правильным")
      return False

    ""Проверка на введение старого пароля""  
    check = verify_password("securepassword", fetched_user.hashed_password)
    if check:
      print("При введении старого пароля считает его верным")
      return False

    ""Проверка на введение неверного пароля""  
    check = verify_password("notsecurepassword", fetched_user.hashed_password)
    if check:
      print("При введении неверного пароля считает его верным")
      return False
      
    print("4/6 тестов пройдены успешно")
    
  except Exception as e:
    print(f'Возникла непредвиденая ошибка. Ошибка: {e}')
    return False

  ""Проверка на удаление пользователя""
  try:
    success = repo.delete_user(fetched_user.id)
    deleted_user = repo.get_user_by_id(fetched_user.id)
    if not deleted_user:
      print("5/6 тестов пройдено верно")
  else:
    print("Ф-ция удаления пользователя не выполняет своего назначения")
    return False

  ""Проверка на создание нескольких пользователей""
  list_of_users = []
  list_of_users_data = [["user@example.com", "securepassword"], ["other@other.ru", "other"], ["user_with_numbers_23@example.com", "1765302"]]
  
  try:
    for i in list of users:
      list_of_users.append(repo.create_user(i[0], i[1]))
    all_users = repo.get_all_users()
    for i in range(len(list_of_users)): 
      if not(list_of_users(i) in all_users):
        print("Пользователь с e-mail {list_of_users_data[i][0]} и паролем {list_of_users_data[i][0]})
        return False
    print("Все тесты пройдены успешно!")
  except Exception as e:
    print(f"Возникла не предвиденная ошибка. Ошибка: {e}")
    return False


if __name__ == "__main__":
    main()
