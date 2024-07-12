import * as React from 'react';
import Box from '@mui/material/Box'
import { TextField } from '@mui/material';

export default class InputBox extends React.Component<{}> {
  public render() {
    return (
      <Box component="form"
            sx={{' & > :not(style)':{m: 1, width: '25ch'},}}
            noValidate
            autoComplete='off'
        >
         <TextField id="outlined-input" label="outlined" variant='outlined'/>

      </Box>
    );
  }
}
