from oscar.apps.catalogue.search_handlers import SimpleProductSearchHandler


class SimpleProductSearchHandler(SimpleProductSearchHandler):
    def get_search_context_data(self, context_object_name):
        # Set the context_object_name instance property as it's needed
        # internally by MultipleObjectMixin
        self.context_object_name = context_object_name
        context = self.get_context_data(object_list=self.object_list.filter(is_active=True).order_by("title"))
        context[context_object_name] = context['page_obj'].object_list
        return context