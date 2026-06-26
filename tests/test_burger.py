import pytest
import data

from unittest.mock import Mock 

from praktikum.burger import Burger
from praktikum.bun import Bun
from praktikum.ingredient import Ingredient



class TestBurger:
    
    def test_get_price_without_bun_raises_error(self):
        burger = Burger()
        with pytest.raises(AttributeError):
            burger.get_price()


    @pytest.mark.parametrize('name, price',[
                             data.black_bun,
                             data.white_bun,
                             data.red_bun])
    def test_set_buns_sets_bun_correctly(self, name, price):
        
        bun = Mock(spec=Bun)
        bun.get_name.return_value = name
        bun.get_price.return_value = price
        
        burger = Burger() 
        burger.set_buns(bun)

        assert burger.bun == bun
        assert burger.bun.get_name() == name
        assert burger.bun.get_price() == price


    def test_set_buns_replaces_previous_bun(self):
        name, price = data.black_bun
        bun1 = Mock(spec=Bun)
        bun1.get_name.return_value = name
        bun1.get_price.return_value = price

        name2, price2 = data.red_bun
        bun2 = Mock(spec=Bun)
        bun2.get_name.return_value = name2
        bun2.get_price.return_value = price2

        burger = Burger()
        burger.set_buns(bun1)
        burger.set_buns(bun2)

        assert burger.bun == bun2
        assert burger.bun.get_name() == name2
        assert burger.bun.get_price() == price2

    
    def test_add_one_ingredient(self):
        
        ingredient = Mock(spec=Ingredient)
                
        burger = Burger()
        burger.add_ingredient(ingredient)
        
        assert burger.ingredients == [ingredient]
        assert len(burger.ingredients) == 1


    def test_add_multiple_ingredients(self):
        
        ingredient_data = data.ingredient_data_3
        count_ingredient = 3

        burger = Burger()
        expected_ingredients = []

        for type_ingredient, name, price in ingredient_data:
            ingredient = Mock(spec=Ingredient)
            ingredient.get_type.return_value = type_ingredient
            ingredient.get_name.return_value = name
            ingredient.get_price.return_value = price
            burger.add_ingredient(ingredient)
            expected_ingredients.append(ingredient)

        assert burger.ingredients == expected_ingredients
        assert len(burger.ingredients) == count_ingredient


    def test_add_two_identical_ingredients(self):
        
        type_ingredient, name, price = data.dinosaur
        
        ingredient1 = Mock(spec=Ingredient)
        ingredient1.get_type.return_value = type_ingredient
        ingredient1.get_name.return_value = name
        ingredient1.get_price.return_value = price

        ingredient2 = Mock(spec=Ingredient)
        ingredient2.get_type.return_value = type_ingredient
        ingredient2.get_name.return_value = name
        ingredient2.get_price.return_value = price

        burger = Burger()
        burger.add_ingredient(ingredient1)
        burger.add_ingredient(ingredient2)

        assert burger.ingredients == [ingredient1, ingredient2]
        assert len(burger.ingredients) == 2



    def test_remove_ingredient_removes_correct_item(self):
        
        type_ingredient, name, price = data.dinosaur
        
        ingredient1 = Mock(spec=Ingredient)
        ingredient1.get_type.return_value = type_ingredient
        ingredient1.get_name.return_value = name
        ingredient1.get_price.return_value = price

        ingredient2 = Mock(spec=Ingredient)
        ingredient2.get_type.return_value = type_ingredient
        ingredient2.get_name.return_value = name
        ingredient2.get_price.return_value = price

        burger = Burger()
        burger.add_ingredient(ingredient1)
        burger.add_ingredient(ingredient2)

        burger.remove_ingredient(0)

        assert burger.ingredients == [ingredient2]
        assert len(burger.ingredients) == 1

    def test_remove_ingredient_from_empty_list_raises_error(self):
        
        burger = Burger()
        
        with pytest.raises(IndexError):
            burger.remove_ingredient(0)


    def test_move_ingredient_changes_order(self):

        ingredient1 = Mock(spec=Ingredient)
        ingredient2 = Mock(spec=Ingredient)
        ingredient3 = Mock(spec=Ingredient)
        
        burger = Burger()
        burger.add_ingredient(ingredient1)
        burger.add_ingredient(ingredient2)
        burger.add_ingredient(ingredient3)

        burger.move_ingredient(0, 2)

        expected = [ingredient2, ingredient3, ingredient1]
        
        assert burger.ingredients == expected


    def test_move_ingredient_to_same_index(self):
        
        ingredient1 = Mock(spec=Ingredient)
        ingredient2 = Mock(spec=Ingredient)
        
        burger = Burger()
        burger.add_ingredient(ingredient1)
        burger.add_ingredient(ingredient2)
        
        burger.move_ingredient(0, 0)
        
        assert burger.ingredients == [ingredient1, ingredient2]


    def test_move_ingredient_from_first_to_last(self):
                
        ingredient1 = Mock(spec=Ingredient)
        ingredient2 = Mock(spec=Ingredient)
        ingredient3 = Mock(spec=Ingredient)
        ingredient4 = Mock(spec=Ingredient)

        burger = Burger()
        burger.add_ingredient(ingredient1)
        burger.add_ingredient(ingredient2)
        burger.add_ingredient(ingredient3)
        burger.add_ingredient(ingredient4)

        burger.move_ingredient(0, 3) 

        assert burger.ingredients == [ingredient2, ingredient3, ingredient4, ingredient1]


    def test_move_ingredient_from_last_to_first(self):
                
        ingredient1 = Mock(spec=Ingredient)
        ingredient2 = Mock(spec=Ingredient)
        
        burger = Burger()
        burger.add_ingredient(ingredient1)
        burger.add_ingredient(ingredient2)
        
        burger.move_ingredient(1, 0) 

        assert burger.ingredients == [ingredient2, ingredient1]

    def test_move_ingredient_from_empty_list_raises_error(self):
        
        burger = Burger()

        with pytest.raises(IndexError):
            burger.move_ingredient(0, 1)

    
    def test_burger_price(self):

        name, price_bun = data.black_bun
        bun = Mock(spec=Bun)
        bun.get_name.return_value = name
        bun.get_price.return_value = price_bun
        
        type_ingredient, name_ingredient, price_ingredient = data.dinosaur
        ingredient = Mock(spec=Ingredient)
        ingredient.get_type.return_value = type_ingredient
        ingredient.get_name.return_value = name_ingredient
        ingredient.get_price.return_value = price_ingredient

        price = price_bun * 2 + price_ingredient

        burger = Burger()
        burger.set_buns(bun)
        burger.add_ingredient(ingredient)
        
        assert burger.get_price() == price


    def test_get_price_with_only_bun(self):
    
        bun = Mock(spec=Bun)
        bun.get_price.return_value = 100
    
        burger = Burger()
        burger.set_buns(bun)
    
        expected_price = 100 * 2
        assert burger.get_price() == expected_price


    @pytest.mark.parametrize('price_buns, price_ingredient',[
                             [100, [100, 100]],
                             [200, [200, 100, 50]], 
                             [100, [100, 100, 300, 200]], 
                             [300, [300, 100, 300, 200, 50]], 
                             [200, [100, 100, 300, 200, 300, 50]]])
    def test_get_price_with_multiple_ingredients(self, price_buns, price_ingredient):
    
        bun = Mock(spec=Bun)
        bun.get_price.return_value = price_buns
    
        burger = Burger()
        burger.set_buns(bun)

        for price in price_ingredient:
            ingredient = Mock(spec=Ingredient)
            ingredient.get_price.return_value = price
            burger.add_ingredient(ingredient)

        expected_price = price_buns * 2 + sum(price_ingredient)

        assert burger.get_price() == expected_price

    
    def test_get_price_after_removing_ingredient(self):
    
        bun = Mock(spec=Bun)
        bun.get_price.return_value = 100
    
        ingredient1 = Mock(spec=Ingredient)
        ingredient1.get_price.return_value = 300
    
        ingredient2 = Mock(spec=Ingredient)
        ingredient2.get_price.return_value = 200
    
        burger = Burger()
        burger.set_buns(bun)
        burger.add_ingredient(ingredient1)
        burger.add_ingredient(ingredient2)
        burger.remove_ingredient(0)
    
        expected_price = 100 * 2 + 200  
        assert burger.get_price() == expected_price

    
    def test_get_receipt(self):
        
        name_bun, price_bun = data.black_bun
        bun = Mock(spec=Bun)
        bun.get_name.return_value = name_bun
        bun.get_price.return_value = price_bun
        
        type_ingredient, name_ingredient, price_ingredient = data.dinosaur
        ingredient = Mock(spec=Ingredient)
        ingredient.get_type.return_value = type_ingredient
        ingredient.get_name.return_value = name_ingredient
        ingredient.get_price.return_value = price_ingredient

        price = price_bun * 2 + price_ingredient

        burger = Burger()
        burger.set_buns(bun)
        burger.add_ingredient(ingredient)

        receipt = burger.get_receipt()

        assert name_bun in receipt 
        assert type_ingredient.lower() in receipt 
        assert name_ingredient in receipt
        assert str(price) in receipt


    def test_get_receipt_format(self):
        name_bun, price_bun = data.black_bun
        bun = Mock(spec=Bun)
        bun.get_name.return_value = name_bun
        bun.get_price.return_value = price_bun

        type_ingredient, name_ingredient, price_ingredient = data.hot_sauce
        ingredient = Mock(spec=Ingredient)
        ingredient.get_type.return_value = type_ingredient
        ingredient.get_name.return_value = name_ingredient
        ingredient.get_price.return_value = price_ingredient

        price = price_bun * 2 + price_ingredient

        burger = Burger()
        burger.set_buns(bun)
        burger.add_ingredient(ingredient)

        receipt = burger.get_receipt()

        expected_lines = [
            f"(==== {name_bun} ====)",
            f"= {type_ingredient.lower()} {name_ingredient} =",
            f"(==== {name_bun} ====)",
            "",
            f"Price: {price}"
        ]

        assert receipt == "\n".join(expected_lines)

    
    def test_get_receipt_without_ingredients(self):
        name_bun, price_bun = data.black_bun
        bun = Mock(spec=Bun)
        bun.get_name.return_value = name_bun
        bun.get_price.return_value = price_bun

        price = price_bun * 2

        burger = Burger()
        burger.set_buns(bun)

        receipt = burger.get_receipt()

        assert name_bun in receipt
        assert str(price) in receipt

    def test_get_receipt_without_bun_raises_error(self):
        burger = Burger()

        with pytest.raises(AttributeError):
            burger.get_receipt()