from models import Category


def make_links_list(categories):
    links_list = []
    for item in categories[1:]:
        node = item.drilldown_tree()[0]['node']
        links_list.append([node.parent, node])
        links_tuple = tuple(tuple(x) for x in links_list)

    return links_tuple


def create_menu_dict(links_tuple):
    menu_dict = {'category_name': 'root', 'category_id': 1, 'subcategories': []}
    name_to_node = {}
    for parent, child in links_tuple:
        parent_node = name_to_node.get(parent)
        if not parent_node:
            name_to_node[parent] = parent_node = {'name': parent.name}
            menu_dict['subcategories'].append(parent_node)
        name_to_node[child] = child_node = {'subcategory_name': child.name, 'category_id': child.id,
                                                                      'items':[{'cost':x.cost, 'name':x.name, 'product_id':x.id}
                                                                                  for x in child.items.all()]}
        parent_node.setdefault('subcategories', []).append(child_node)

    return menu_dict


categories = Category.query.order_by(Category.id).all()
links_tuple = make_links_list(categories)
menu_dict = create_menu_dict(links_tuple)
