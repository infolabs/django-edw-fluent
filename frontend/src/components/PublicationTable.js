import React, { Component } from 'react';
import TableItemMixin from 'components/BaseEntities/TableItemMixin';


// Container
export default class Table extends Component {
    render_table_headers(table_titles) {
        return (
            <thead>
            <tr>
              {Object.entries(table_titles).map(
                  ([key_name, field], i)=>
                      <th key={i}>{field}</th>)}
              </tr>
            </thead>);
    }

    render() {
        const { items, actions, loading, descriptions, meta } = this.props;

        const table_titles = this.render_table_headers(meta.extra.table_titles);

        return(
            <div className="ex-base-table">
              <table className='table'>
                  {table_titles}
                  <tbody>
                    {items.map(
                      (child, i) =>
                      <TableItem
                          key={i}
                          data={child}
                          actions={actions}
                          loading={loading}
                          descriptions={descriptions}
                          position={i}
                          meta={meta}
                      />)}
                  </tbody>
              </table>
            </div>);
    }
}

class TableItem extends TableItemMixin(Component) {

    getDescriptionBaloon(data, marks, characteristics) {
    if (marks.length) {
        this.state.isHaveDescription = true;

        return (
            <div className="ex-description-wrapper">
              <div className="ex-baloon">
                {this.state.v_pos === 'top' &&
                <div className="ex-baloon-arrow">
                    <div className="ex-arrow"/>
                </div>
                }
                <ul className="ex-attrs">
                {characteristics.map(
                  (child, i) => {
                    return (
                      <li data-path={child.path} key={i}
                          data-view-class={child.view_class.join(" ")}>
                        <strong>{child.name}:&nbsp;</strong>
                        {child.values.join(", ")}
                      </li>
                    )
                  }
                )}
                </ul>
                <ul className="ex-baloon-ribbons">
                  {marks.map(
                    (child, i) =>
                      <li className="ex-baloon-ribbon"
                          key={i}
                          data-name={child.name}
                          data-path={child.path}
                          data-view-class={child.view_class.join(' ')}>
                        <div className="ex-baloon-ribbon">{child.values.join(', ')}</div>
                      </li>
                  )}
                </ul>
                {this.state.v_pos === 'bottom' &&
                <div className="ex-baloon-arrow">
                    <div className="ex-arrow"/>
                </div>
                }
              </div>
            </div>
            );
    }
  }

    renderDate(data) {
        const date = new Date(data.extra.created_at).toLocaleDateString()
        return(
            <td className="table-element">
              <i className="fa fa-calendar"/>&nbsp;
              {date}
            </td>);
    }

    getRenderFields() {
        return{
            'entity_name': this.renderTitle.bind(this),
            'media': this.renderMedia.bind(this),
            'extra.created_at': this.renderDate.bind(this),
            'default': this.renderDefault.bind(this),
            'short_marks': this.renderEllipsis.bind(this)
        }
    }

    render() {
        const { data, position, meta, descriptions } = this.props;

         let characteristics = data.short_characteristics || [],
             marks = data.short_marks || [];

         if (descriptions[data.id]) {
          characteristics = descriptions[data.id].characteristics || [];
          marks = descriptions[data.id].marks || [];
        }

        const descriptionBaloon = this.getDescriptionBaloon(data, marks, characteristics) || "",
            itemContent = this.getItemContent(data, meta.extra.table_titles, descriptionBaloon),
            itemBlock = this.getItemBlock(itemContent);

            return (
                <>{itemBlock}</>
            );
        };
}