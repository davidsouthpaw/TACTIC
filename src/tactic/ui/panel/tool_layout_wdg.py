###########################################################
#
# Copyright (c) 2009, Southpaw Technology
#                     All Rights Reserved
#
# PROPRIETARY INFORMATION.  This software is proprietary to
# Southpaw Technology, and is not to be reproduced, transmitted,
# or disclosed in any way without written permission.
#
#
#
__all__ = ["ToolLayoutWdg"]

from pyasm.common import Common
from pyasm.search import Search, SearchKey
from pyasm.web import DivWdg, Table
from pyasm.widget import ThumbWdg, IconWdg
from tactic.ui.container import SmartMenu

from table_layout_wdg import FastTableLayoutWdg
from tactic.ui.widget import IconButtonWdg, SingleButtonWdg

class ToolLayoutWdg(FastTableLayoutWdg):

    ARGS_KEYS = {
        "search_type": {
            'description': "search type that this panels works with",
            'type': 'TextWdg',
            'order': 0,
            'category': 'Required'
        },
    } 


    def get_display(my):

        my.view_editable = True

        if my.kwargs.get("do_search") != "false":
            my.handle_search()

        my.kwargs['show_gear'] = 'false'


        # set the sobjects to all the widgets then preprocess
        for widget in my.widgets:
            widget.set_sobjects(my.sobjects)
            widget.set_parent_wdg(my)
            # preprocess the elements
            widget.preprocess()



        # extraneous variables inherited from TableLayoutWdg
        my.edit_permission = False

        top = DivWdg()
        my.set_as_panel(top)
        top.add_class("spt_sobject_top")

        inner = DivWdg()
        top.add(inner)
        inner.add_color("background", "background")
        inner.add_color("color", "color")
        inner.add_class("spt_table")
        inner.add_class("spt_layout")
        inner.add_attr("spt_version", "2")


        from tactic.ui.input import Html5UploadWdg
        upload_wdg = Html5UploadWdg()
        inner.add(upload_wdg)
        my.upload_id = upload_wdg.get_upload_id()

        # set up the context menus
        menus_in = {
            'DG_HEADER_CTX': [ my.get_smart_header_context_menu_data() ],
            'DG_DROW_SMENU_CTX': [ my.get_data_row_smart_context_menu_details() ]
        }
        SmartMenu.attach_smart_context_menu( inner, menus_in, False )


        thumb = ThumbWdg()
        thumb.handle_layout_behaviors(inner)

        is_refresh = my.kwargs.get("is_refresh")
        if my.kwargs.get("show_shelf") not in ['false', False]:
            action = my.get_action_wdg()
            inner.add(action)

        content = DivWdg()
        inner.add( content )
        content.add( my.get_content_wdg() )


        # NOTE: a lot of scaffolding to convince that search_cbk that this
        # is a proper layout
        top.add_class("spt_table_top");
        class_name = Common.get_full_class_name(my)
        top.add_attr("spt_class_name", class_name)


        # NOTE: adding a fake header to conform to a table layout.  Not
        # sure if this is the correct interface for this
        header_row_div = DivWdg()
        header_row_div.add_class("spt_table_header_row")
        content.add(header_row_div)
        content.add_class("spt_table_table");

        my.handle_load_behaviors(content)


        inner.add_class("spt_table_content");
        inner.add_attr("spt_search_type", my.kwargs.get('search_type'))
        inner.add_attr("spt_view", my.kwargs.get('view'))


        limit_span = DivWdg()
        inner.add(limit_span)
        limit_span.add_style("margin-top: 4px")
        limit_span.add_class("spt_table_search")
        limit_span.add_style("width: 250px")
        limit_span.add_style("margin: 5 auto")

        info = my.search_limit.get_info()
        if info.get("count") == None:
            info["count"] = len(my.sobjects)


        from tactic.ui.app import SearchLimitSimpleWdg
        limit_wdg = SearchLimitSimpleWdg(
            count=info.get("count"),
            search_limit=info.get("search_limit"),
            current_offset=info.get("current_offset"),
        )
        inner.add(limit_wdg)


        my.add_layout_behaviors(inner)

        if my.kwargs.get("is_refresh") == 'true':
            return inner
        else:
            return top


    def add_layout_behaviors(my, layout_wdg):

        layout_wdg.add_relay_behavior( {
            'type': 'click',
            'bvr_match_class': 'spt_item_content',
            'cbjs_action': '''
            spt.tab.set_main_body_tab();
            var top = bvr.src_el.getParent(".spt_item_top");
            var search_key = top.getAttribute("spt_search_key");
            var name = top.getAttribute("spt_name");
            var search_code = top.getAttribute("spt_search_code");
            var class_name = 'tactic.ui.tools.SObjectDetailWdg'
            var kwargs = {
                search_key: search_key
            }
            spt.tab.add_new(search_code, name, class_name, kwargs);
            '''
        } )

        bg1 = layout_wdg.get_color("background3")
        bg2 = layout_wdg.get_color("background3", 5)
        layout_wdg.add_relay_behavior( {
            'type': 'mouseover',
            'bvr_match_class': 'spt_item_top',
            'cbjs_action': '''
            bvr.src_el.setStyle("opacity", "0.8");
            var el = bvr.src_el.getElement(".spt_tile_title");
            if (el) {
                el.setStyle("background", "%s");
            }
            ''' % bg2
        } )

        layout_wdg.add_relay_behavior( {
            'type': 'mouseout',
            'bvr_match_class': 'spt_item_top',
            'cbjs_action': '''
            bvr.src_el.setStyle("opacity", "1.0");
            var el = bvr.src_el.getElement(".spt_tile_title");
            if (el) {
                el.setStyle("background", "%s");
            }
            ''' % bg1
        } )





    def get_content_wdg(my):

        div = DivWdg()
        div.add_class("spt_tool_top")

        table = Table()
        div.add(table)
        table.add_row()

        td = table.add_cell()
        from table_layout_wdg import FastTableLayoutWdg

        kwargs = my.kwargs.copy()


        td.add_style("width: 1%")
        td.add_style("vertical-align: top")
        layout_div = DivWdg()
        layout_div.add_style("min-height: 500px")
        td.add(layout_div)

        my.kwargs['element_names'] = ['name','description','detail', 'file_list','general_checkin']
        my.kwargs['show_shelf'] = False
        layout = FastTableLayoutWdg(**my.kwargs)
        layout_div.add(layout)


        td = table.add_cell()
        td.add_border()
        td.add_style("vertical-align: top")

        content = DivWdg()
        td.add(content)
        content.add_class("spt_tool_content")
        #content.add_style("margin: -1px")


        no_content_wdg = DivWdg()
        content.add(no_content_wdg)
        no_content_wdg.add("<br/>"*3)
        no_content_wdg.add("<i>-- No Content --</i>")
        #no_content_wdg.add_style("opacity: 0.5")
        no_content_wdg.add_style("margin: 30px auto")
        no_content_wdg.add_color("color", "color3")
        no_content_wdg.add_color("background", "background3")
        no_content_wdg.add_style("text-align", "center")
        no_content_wdg.add_style("padding-top: 20px")
        no_content_wdg.add_style("padding-bottom: 20px")
        no_content_wdg.add_style("width: 350px")
        no_content_wdg.add_style("height: 110px")
        no_content_wdg.add_border()


        return div







__all__ = ['CustomLayoutWithSearchWdg']
from custom_layout_wdg import CustomLayoutWdg
class CustomLayoutWithSearchWdg(ToolLayoutWdg):

    ARGS_KEYS = CustomLayoutWdg.ARGS_KEYS.copy()
    ARGS_KEYS['search_type'] = 'search type of the sobject to be displayed'

    def get_content_wdg(my):
        kwargs = my.kwargs.copy()
        layout = CustomLayoutWdg(**kwargs)
        layout.set_sobjects(my.sobjects)
        return layout




__all__ = ['CustomItemLayoutWithSearchWdg']
class CustomItemLayoutWithSearchWdg(ToolLayoutWdg):

    ARGS_KEYS = CustomLayoutWdg.ARGS_KEYS.copy()
    ARGS_KEYS['search_type'] = 'search type of the sobject to be displayed'

    def get_content_wdg(my):
        div = DivWdg()
        for sobject in my.sobjects:
            kwargs = my.kwargs.copy()
            layout = CustomLayoutWdg(**kwargs)
            layout.set_sobjects(my.sobjects)
            layout.set_sobject(sobject)
            div.add(layout)
        return div





__all__ = ['RepoBrowserLayoutWdg']
class RepoBrowserLayoutWdg(ToolLayoutWdg):

    ARGS_KEYS = CustomLayoutWdg.ARGS_KEYS.copy()
    ARGS_KEYS['search_type'] = 'search type of the sobject to be displayed'

    def get_content_wdg(my):
        from tactic.ui.tools import RepoBrowserWdg
        kwargs = my.kwargs.copy()
        layout = RepoBrowserWdg(**kwargs)
        layout.set_sobjects(my.sobjects)
        return layout




__all__ = ['CardLayoutWdg']
class CardLayoutWdg(ToolLayoutWdg):

    ARGS_KEYS = CustomLayoutWdg.ARGS_KEYS.copy()
    ARGS_KEYS['search_type'] = 'search type of the sobject to be displayed'

    def get_content_wdg(my):
        div = DivWdg()

        inner = DivWdg()
        div.add(inner)

        # set up the context menus
        menus_in = {
            #'DG_HEADER_CTX': [ my.get_smart_header_context_menu_data() ],
            'DG_DROW_SMENU_CTX': [ my.get_data_row_smart_context_menu_details() ]
        }
        SmartMenu.attach_smart_context_menu( inner, menus_in, False )

        for sobject in my.sobjects:
            inner.add(my.get_item_wdg(sobject))

        return div


    def get_item_wdg(my, sobject):

        div = DivWdg()
        div.add_class("spt_item_top")
        div.add_style("padding: 10px")
        SmartMenu.assign_as_local_activator( div, 'DG_DROW_SMENU_CTX' )
        div.add_class("spt_table_row")
        div.add_attr("spt_search_key", sobject.get_search_key(use_id=True))
        div.add_attr("spt_search_code", sobject.get_code())
        name = sobject.get_value("name", no_exception=True)
        if not name:
            name = sobject.get_code()
        div.add_attr("spt_name", name)

        table = Table()
        div.add(table)
        table.set_max_width()
        tr = table.add_row()

        width = my.kwargs.get("preview_width")
        if not width:
            width = "240px"

        td = table.add_cell()
        td.add_style("width: %s" % width);
        td.add_style("vertical-align: top")


        from tile_layout_wdg import ThumbWdg2
        thumb_div = DivWdg()
        td.add(thumb_div)
        thumb_div.add_border()
        thumb_div.add_color("background", "background", 5)
        thumb_div.add_border()
        thumb_div.add_class("spt_item_content")

        thumb = ThumbWdg2()
        thumb_div.add(thumb)
        thumb.set_sobject(sobject)

        info_div = my.get_info_wdg(sobject)
        td = table.add_cell(info_div)
        td.add_style("vertical-align: top")


        return div


    def get_info_wdg(my, sobject):

        div = DivWdg()
        div.add_style("margin: 0px 20px 20px 20px")
        div.add_style("padding: 20px")
        div.add_color("background", "background3")
        div.add_color("color", "color3")
        div.set_round_corners(5)

        element_names = my.kwargs.get("element_names")
        if not element_names:
            element_names = ["code","name","description",]
        else:
            element_names = element_names.split(",")


        view = "table"

        from pyasm.widget import WidgetConfigView
        search_type = sobject.get_search_type()
        config = WidgetConfigView.get_by_search_type(search_type, view)


        table = Table()
        div.add(table)
        for element_name in element_names:
            table.add_row()
            title = Common.get_display_title(element_name)
            td = table.add_cell("%s: " % title)
            td.add_style("width: 200px")
            td.add_style("padding: 5px")


            element = config.get_display_widget(element_name)
            element.set_sobject(sobject)
            element.preprocess()
            td = table.add_cell(element)
            td.add_style("padding: 5px")
            #value = sobject.get_value(element_name, no_exception=True) or "N/A"
            #table.add_cell(value)

        div.add("<br/>")
        from tactic.ui.widget import DiscussionWdg
        notes_wdg = DiscussionWdg()
        notes_wdg.set_sobject(sobject)
        div.add(notes_wdg)

        return div


