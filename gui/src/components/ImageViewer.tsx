import * as React from 'react';
import './ImageViewer.css';

import { ImageProperties } from '../constants';

// export interface Props {
//   url: string;
//   alt?: string;
//   width: number;
//   height: number
// }

export const ImageViewer = (props: ImageProperties) => {
  const img = new Image(props.height, props.width);
  img.src = props.url;
  

  return (
    <div className="img-right">
      <img src={img.src} height={img.height} width={img.width} />
    </div>
  )
}

