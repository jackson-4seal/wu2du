# Wu2Du - Design

## Overview

Outside of creating an account and logging in, the app largely functions on one page. The page will display the account and site information at the top nav bar, all user todo lists in a lower bar, and the items in the current to do list as the main centered content on the page.

## List creation

Logged in users will see a " + create list " button on the top nav bar. Clicking will access a route yet to be created


## List grabbing

in lists.py, index function at "/". Takes an optional parameter of a list id for which to render its items. Default value is the oldest measured by the created field. Default value will be checked with  `if list_to_get is None:`

The index route itself just gets a list of all todo lists for the user and all items for the given list_to_get. It then passes these values to the render_template index.html.

index.html extends base.html. 

Index will create a list selector div for each list passed. Each list selector needs to be given a width style value of (100 / len(lists))%. List selectors are hyperlink elements that on click recursively call index, passing their list id to the route. While creating list selectors, if the current id matches the list id of any of the items (they all share the same list_id), the selector will be given an html id to indicate that it should look different since its the current displayed list.

Index will also create a list item div for each item in items. Each item will be given a text, checkbox (using complete field), and maybe a due date if I change the current schema (3/14). SQL statement should sort items with complete items first so all complete todoitems will appear at the top.



## Post updating

When a user clicks to edit text, change a due date, or mark an item as finished or unfinished, the click will call the updating endpoint that has yet to be created.

## Post deleting

When a user clicks the 'x' button on the far right, the click will call the delete post endpoint that has yet to be created.

## List updating (todo item creation)

When a user clicks to add a todo item, the click will call the addtolist endpoint that has yet to be created.

## List deleting

When a user clicks the x by the corresponding list in the todo list nav bar, they will be prompted to make sure they want to delete the list. Once they confirm, the delete list endpoint will be called, removing all database todoitems associated with the list before deleting the list itself. This endpoint has yet to be created.

