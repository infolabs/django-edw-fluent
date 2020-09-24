import React, { Component } from 'react';
import ListItemMixin from 'components/BaseEntities/ListItemMixin';


const getDate = (date, offset = 3) => {
  let m = new Date(date);
  m.setHours(m.getHours() + offset);
  return(`${('0' + m.getUTCDate()).slice(-2)}.${('0' + (m.getUTCMonth() + 1)).slice(-2)}.${m.getUTCFullYear()}`);
};

// Container

export default class PublicationList extends Component {

  render() {
    const { items, actions, loading, descriptions, meta } = this.props;
    let entities_class = "entities list-items";
    entities_class = loading ? entities_class + " ex-state-loading" : entities_class;

    return (
      <div className={entities_class}>
        {items.map(
          (child, i) =>
          <PublicationListItem
              key={i}
              data={child}
              actions={actions}
              loading={loading}
              descriptions={descriptions}
              position={i}
              meta={meta}
          />
        )}
      </div>
    );
  }
}

// Element

class PublicationListItem extends ListItemMixin(Component) {

  getDescriptionText() {
    const { data, descriptions } = this.props,
        descr = descriptions[data.id];

    return descr && descriptions.opened[data.id] ? descr.subtitle || descr.lead : data.extra.short_subtitle;
  }

  static isEqualStr(s1, s2) {
    s1 = s1.replace(/\s+/g, '');
    s2 = s2.replace(/\s+/g, '');

    return s1 === s2;
  }

  getItemBlock(url, data, title, descrText, descriptions){
    const characteristics = data.short_characteristics;

    return (
      <div className="col-md-9">
        <a href={url}>
          <h4>{title}</h4>
          {
            !PublicationListItem.isEqualStr(descrText, data.entity_name) &&
            <p>{descrText}</p>
          }
        </a>
        {descriptions.opened[data.id] && characteristics.length &&
        <div className="ex-description-wrapper">
          <ul className="ex-attrs">
            {characteristics.map((child, i) => (
              <li data-path={child.path} key={i} data-view-class={child.view_class.join(" ")}>
                <strong>{child.name}:&nbsp;</strong>
                {child.values.join(';')}
              </li>
            ))}
          </ul>
        </div>
        }
        <p className="date_time"><i className="fa fa-calendar"/>&nbsp;{getDate(data.extra.created_at)}</p>
        <span className="padding-left-10 sub-statisitic"><i className="fa fa-eye" aria-hidden="true" />&nbsp;{data.extra.statistic}</span>
      </div>
    )
  }

  render() {
    const { data, meta, descriptions } = this.props,
          url = data.extra && data.extra.url ? data.extra.url : data.entity_url,
          groupSize = data.extra && data.extra.group_size ? data.extra.group_size : 0,
          descrText = this.getDescriptionText();


    let groupDigit = "";
    if (groupSize) {
      groupDigit = (
        <div className="ex-pack">
          <span className="ex-digit">{groupSize}</span>
          <div><div><div></div></div></div>
        </div>
      );
    }

    let characteristics = data.short_characteristics || [],
        marks = data.short_marks || [];

    // let related_data_marts = [];
    if (descriptions[data.id]) {
      characteristics = descriptions[data.id].characteristics || [];
      marks = descriptions[data.id].marks || [];
      // related_data_marts = descriptions[data.id].marks || [];
    }

    const className = "ex-catalog-item list-item" + (groupSize ? " ex-catalog-item-variants" : "") +
        (descriptions.opened[data.id] ? " ex-state-description" : "");

    const title = groupSize && !meta.alike ? data.extra.group_name : data.entity_name,
          itemBlock = this.getItemBlock(url, data, title, descrText, descriptions),
          itemContent = this.getItemContent(url, data, itemBlock, marks);

    return (
      <div className={className}
         onMouseOver={e => this.handleMouseOver(e)}
         onMouseOut={e => this.handleMouseOut(e)}
         style={{minHeight: this.state.minHeight}}>
        {groupDigit}
        {itemContent}
      </div>
    );
  }
}
