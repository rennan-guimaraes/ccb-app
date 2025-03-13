"""
Pacote de interface do usuário para a aplicação Gestão Vista.
Contém componentes, estilos e utilitários para a interface gráfica.
"""

from gestao_vista.ui.styles import setup_styles
from gestao_vista.ui.components import (
    create_button,
    create_label,
    create_sidebar,
    create_controls,
    create_combobox,
    create_dialog_window,
    create_entry,
    create_form_field,
)

# Importar correções específicas para Windows
from gestao_vista.ui.windows_fixes import (
    apply_windows_specific_fixes,
    get_asset_path,
    fix_treeview_header_for_windows,
)

__all__ = [
    "setup_styles",
    "create_button",
    "create_label",
    "create_sidebar",
    "create_controls",
    "create_combobox",
    "create_dialog_window",
    "create_entry",
    "create_form_field",
    "apply_windows_specific_fixes",
    "get_asset_path",
    "fix_treeview_header_for_windows",
]
