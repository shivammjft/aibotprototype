import * as React from 'react';
import { DataGrid, GridColDef } from '@mui/x-data-grid';
import Paper from '@mui/material/Paper';

const columns = [
  { field: 'id', headerName: 'Session Id', width: 120 },
  { field: 'query_text_bot', headerName: 'Quert Text Bot', width: 180 },
  { field: 'query_text_user', headerName: 'Query Text User', width: 180 },
  {
    field: 'query_context',
    headerName: 'Query Context',
    type: 'string',
    width: 180,
  },
  {
    field: 'query_time',
    headerName: 'Query Time',
    description: 'This column has a value getter and is not sortable.',
    width: 180,
  },
  {
    field: 'origin_url',
    headerName: 'Origin URL',
    type: 'string',
    width: 180,
  },
  {
    field: 'input_tokens',
    headerName: 'Input Tokens',
    type: 'number',
    width: 100,
  },
  {
    field: 'output_tokens',
    headerName: 'Output Tokens',
    type: 'number',
    width: 110,
  },
];

// const rows = [
//   {
//     id: 'session_124',
//     query_text_bot: 'What are your hours?',
//     query_text_user: 'What time do you open?',
//     query_context: 'business hours inquiry',
//     query_time: '2024-09-09T12:10:00',
//     origin_url: 'https://example1.com/',
//     input_tokens: 45,
//     output_tokens: 15,
//   },
//   {
//     id: 'session_124',
//     query_text_bot: 'What are your hours?',
//     query_text_user: 'What time do you open?',
//     query_context: 'business hours inquiry',
//     query_time: '2024-09-09T12:10:00',
//     origin_url: 'https://example1.com/',
//     input_tokens: 45,
//     output_tokens: 15,
//   },
//   {
//     id: 'session_124',
//     query_text_bot: 'What are your hours?',
//     query_text_user: 'What time do you open?',
//     query_context: 'business hours inquiry',
//     query_time: '2024-09-09T12:10:00',
//     origin_url: 'https://example1.com/',
//     input_tokens: 45,
//     output_tokens: 15,
//   },
//   {
//     id: 'session_124',
//     query_text_bot: 'What are your hours?',
//     query_text_user: 'What time do you open?',
//     query_context: 'business hours inquiry',
//     query_time: '2024-09-09T12:10:00',
//     origin_url: 'https://example1.com/',
//     input_tokens: 45,
//     output_tokens: 15,
//   },
//   {
//     id: 'session_124',
//     query_text_bot: 'What are your hours?',
//     query_text_user: 'What time do you open?',
//     query_context: 'business hours inquiry',
//     query_time: '2024-09-09T12:10:00',
//     origin_url: 'https://example1.com/',
//     input_tokens: 45,
//     output_tokens: 15,
//   },
//   {
//     id: 'session_124',
//     query_text_bot: 'What are your hours?',
//     query_text_user: 'What time do you open?',
//     query_context: 'business hours inquiry',
//     query_time: '2024-09-09T12:10:00',
//     origin_url: 'https://example1.com/',
//     input_tokens: 45,
//     output_tokens: 15,
//   },
//   {
//     id: 'session_124',
//     query_text_bot: 'What are your hours?',
//     query_text_user: 'What time do you open?',
//     query_context: 'business hours inquiry',
//     query_time: '2024-09-09T12:10:00',
//     origin_url: 'https://example1.com/',
//     input_tokens: 45,
//     output_tokens: 15,
//   },
//   {
//     id: 'session_124',
//     query_text_bot: 'What are your hours?',
//     query_text_user: 'What time do you open?',
//     query_context: 'business hours inquiry',
//     query_time: '2024-09-09T12:10:00',
//     origin_url: 'https://example1.com/',
//     input_tokens: 45,
//     output_tokens: 15,
//   },
//   {
//     id: 'session_124',
//     query_text_bot: 'What are your hours?',
//     query_text_user: 'What time do you open?',
//     query_context: 'business hours inquiry',
//     query_time: '2024-09-09T12:10:00',
//     origin_url: 'https://example1.com/',
//     input_tokens: 45,
//     output_tokens: 15,
//   },
//   {
//     id: 'session_124',
//     query_text_bot: 'What are your hours?',
//     query_text_user: 'What time do you open?',
//     query_context: 'business hours inquiry',
//     query_time: '2024-09-09T12:10:00',
//     origin_url: 'https://example1.com/',
//     input_tokens: 45,
//     output_tokens: 15,
//   },
//   {
//     id: 'session_124',
//     query_text_bot: 'What are your hours?',
//     query_text_user: 'What time do you open?',
//     query_context: 'business hours inquiry',
//     query_time: '2024-09-09T12:10:00',
//     origin_url: 'https://example1.com/',
//     input_tokens: 45,
//     output_tokens: 15,
//   },
//   {
//     id: 'session_124',
//     query_text_bot: 'What are your hours?',
//     query_text_user: 'What time do you open?',
//     query_context: 'business hours inquiry',
//     query_time: '2024-09-09T12:10:00',
//     origin_url: 'https://example1.com/',
//     input_tokens: 45,
//     output_tokens: 15,
//   },
// ];

const paginationModel = { page: 0, pageSize: 5 };

export default function ChatBotQueryTable({ queries }) {
  const [rows, setRows] = React.useState([]);

  React.useEffect(() => {
    setRows(queries);
  }, [queries]);

  return (
    <div className="mt-[2rem] flex items-center ">
      <Paper sx={{ height: 400, width: '74%' }}>
        <DataGrid
          rows={rows}
          columns={columns}
          initialState={{ pagination: { paginationModel } }}
          pageSizeOptions={[5, 10]}
          checkboxSelection
          sx={{ border: 0 }}
        />
      </Paper>
    </div>
  );
}
