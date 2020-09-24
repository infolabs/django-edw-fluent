import React, {Component} from 'react';
import TileItemMixin from 'components/BaseEntities/TileItemMixin';


// Container

export default class PublicationTile extends Component {

  render() {
    const {items, actions, loading, descriptions, meta} = this.props;
    let entities_class = "entities ex-tiles";
    entities_class = loading ? entities_class + " ex-state-loading" : entities_class;

    return (
      <ul className={entities_class}>
        {items.map(
          (child, i) =>
            <PublicationTileItem key={i} data={child} actions={actions} descriptions={descriptions} position={i}
                                 meta={meta}/>
        )}
      </ul>
    );
  }
}

// Element

class PublicationTileItem extends TileItemMixin(Component) {

  toggleDescription(e) {
    const {data, actions, descriptions} = this.props,
      id = data.id;

    if (this.getIsHover(e.clientX, e.clientY)) {
      actions.showDescription(id);
      if (!descriptions[id])
        actions.getEntityItem(data);
    } else
      actions.hideDescription(id);
  }

  getDescriptionText() {
    const {data, descriptions} = this.props,
      descr = descriptions[data.id];

    return descr && descriptions.opened[data.id] ? descr.subtitle || descr.lead : data.extra.short_subtitle;
  }

  static isEqualStr(s1, s2) {
    s1 = s1 && s1.replace(/\s+/g, '');
    s2 = s2 && s2.replace(/\s+/g, '');

    return s1 === s2;
  }

  getDescriptionBaloon(data, characteristics, descrText, checkDescrText) {
    const created_at = new Date(data.extra.created_at);

    return (
      <div className="ex-description-wrapper">
        <div className="ex-baloon">
          <div className="ex-arrow"/>
          <ul className="ex-attrs">
            {!checkDescrText && <li><strong>{descrText}</strong></li>}
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
          <div className="publication-extra">
            <hr/>
            <strong><i className="fa fa-calendar" aria-hidden="true"></i></strong>&nbsp;
            {created_at.getDate() > 9 ? created_at.getDate() : '0' + created_at.getDate()}.
            {created_at.getMonth() + 1 > 9 ? created_at.getMonth() + 1 : '0' + (created_at.getMonth() + 1)}.
            {created_at.getFullYear()}
            <strong className="second"><i className="fa fa-eye" aria-hidden="true"></i></strong>&nbsp;
            {data.extra.statistic}
          </div>
        </div>
      </div>
    )
  }

  getItemBlock(descriptionBaloon, itemContent) {
    return (
      <div className="ex-catalog-item-block">
        {descriptionBaloon}
        {itemContent}
      </div>
    )
  }

  render() {
    const {data, descriptions, position, meta} = this.props,
      index = position + meta.offset,
      descrText = this.getDescriptionText(),
      checkDescrText = PublicationTileItem.isEqualStr(descrText, data.entity_name);

    let liClass = "ex-catalog-item";
    if (descriptions.opened[data.id])
      liClass += " ex-state-description";

    let characteristics = data.short_characteristics || [],
      marks = data.short_marks || [];

    // let related_data_marts = [];
    if (descriptions[data.id]) {
      characteristics = descriptions[data.id].characteristics || [];
      marks = descriptions[data.id].marks || [];
      // related_data_marts = descriptions[data.id].marks || [];
    }

    const descriptionBaloon = this.getDescriptionBaloon(data, characteristics, descrText, checkDescrText) || "",
      title = data.entity_name,
      itemContent = this.getItemContent(data, title, marks),
      itemBlock = this.getItemBlock(descriptionBaloon, itemContent);

    return (
      <li className={liClass}
          data-horizontal-position={this.state.h_pos}
          data-vertical-position="center"
          data-index={index}
          onMouseOver={e => {
            ::this.handleMouseOver(e)
          }}
          onMouseOut={e => {
            ::this.handleMouseOut(e)
          }}>
        {itemBlock}
      </li>
    );
  }
}