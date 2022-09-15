import React, {useState, useEffect} from 'react';
import './App.css';
import {LocalizationProvider} from '@mui/x-date-pickers';
import {MobileTimePicker} from '@mui/x-date-pickers';
import {AdapterDateFns} from '@mui/x-date-pickers/AdapterDateFns';
import {Box, BoxProps, useTheme} from "@material-ui/core";


import {Grid, Stack, TextField, ToggleButtonGroup} from "@mui/material";
import Slider from '@mui/material/Slider';

import {ThemeProvider, createTheme} from '@mui/material/styles';
import {ToggleButton} from "@mui/lab";
import * as PropTypes from "prop-types";

const darkTheme = createTheme({
    palette: {
        mode: 'dark',
    },
});

const marks = [
    {
        value: 0,
        label: '0°C',
    },
    {
        value: 20,
        label: '20°C',
    },
    {
        value: 37,
        label: '37°C',
    },
    {
        value: 100,
        label: '100°C',
    },
];

const marks_delta = [
    {
        value: 1,
        label: '1°C',
    },
    {
        value: 4,
        label: '4°C',
    },
    {
        value: 7,
        label: '7°C',
    },
    {
        value: 10,
        label: '10°C',
    },
];

// type Props = BoxProps & {
//   x//?: number; // multiplier of theme.spacing
//   y//?: number; // multiplier of theme.spacing
//   basis//?: number; // multiplier of theme.spacing
// };

const Spacer = ({x, y, basis, ...restProps}) => {
    const theme = useTheme();
    return (
        <Box
            data-testid="Spacer"
            width={x ? theme.spacing(x) : undefined}
            height={y ? theme.spacing(y) : undefined}
            flexBasis={basis ? theme.spacing(basis) : undefined}
            flexGrow={0}
            flexShrink={0}
            {...restProps}
        />
    );
};

function valuetext(value) {
    return `${value}°C`;
}

function createSwitch(name, switchNumber, offText, onText) {
    return <>
        <Grid item xs={12} container spacing={2} alignItems={"center"}>
            <Grid item xs={7}>
                {name}
            </Grid>
            <Grid item xs={2}>
                {ColorToggleButton(switchNumber, offText, onText)}
            </Grid>
        </Grid>
    </>;
}

function ColorToggleButton(switchNumber, off = "AUS", on = "EIN") {
    const [state, setState] = React.useState("0");

    useEffect(() => {
        fetch('/switches').then(res => res.json()).then(data => {
            setState(data[switchNumber]);
        });
    }, []);

    const handleChange = (
        event, //: React.MouseEvent<HTMLElement>,
        state //: string,
    ) => {
        const requestOptions = {
            method: 'POST',
            headers: {'Content-Type': 'application/json'}
        };
        if (state != null) {
            fetch(`/switch?switch_id=${encodeURIComponent(switchNumber)}&target_state=${encodeURIComponent(state)}`,
                requestOptions).then(response => response.json())
            setState(state);
        }

    }

    return (
        <ToggleButtonGroup
            color="primary"
            value={state}
            exclusive
            onChange={handleChange}
        >
            <ToggleButton value="0">{off}</ToggleButton>
            <ToggleButton value="1">{on}</ToggleButton>
        </ToggleButtonGroup>
    );
}

function GlobalToggle() {
    const [alignment, setAlignment] = React.useState('off');

    const handleChange = (
        event, //: React.MouseEvent<HTMLElement>,
        newAlignment //: string,
    ) => {
        if (newAlignment != null) {
            setAlignment(newAlignment);
        }
    };

    return (
        <ToggleButtonGroup
            color="primary"
            value={alignment}
            exclusive
            onChange={handleChange}
        >
            <ToggleButton value="off">Aus</ToggleButton>
            <ToggleButton value="on">Ein</ToggleButton>
            <ToggleButton value="auto">Automatik</ToggleButton>
        </ToggleButtonGroup>
    );
}

function Item(props) {
    return null;
}

Item.propTypes = {children: PropTypes.node};

function App() {
    const [currentTime, setCurrentTime] = useState(0);
    const [value, setValue] = useState(0);

    useEffect(() => {
        fetch('/time').then(res => res.json()).then(data => {
            setCurrentTime(data.time);
        });
    }, []);

    return (
        <ThemeProvider theme={darkTheme}>
            <div className="App">
                <header className="App-header">
                    <Grid container spacing={2} direction={"column"}>
                        <Grid item xs={12}>
                            <h1>Demax Heizungssteuerung</h1>
                        </Grid>
                        <Grid item xs={12} container alignItems={"center"} spacing={2}>
                            <Grid item xs={4}>
                            </Grid>
                            <Grid item xs={2}>
                                Heizung
                            </Grid>
                            <Grid item xs={2}>
                                {GlobalToggle()}
                            </Grid>
                            <Grid item xs={4}>
                            </Grid>
                        </Grid>

                        <Grid item xs={12} container spacing={2} direction={"column"}>

                            <Grid item xs={12} container alignItems={"flex-start"} spacing={2}>

                                <Grid item xs={1}/>
                                <Grid item xs={5} container direction={"column"} spacing={1}>
                                    <Grid item xs={12}><h2>Aktoren</h2></Grid>
                                    {createSwitch("Ladepumpe", "1")}
                                    {createSwitch("Heizen/Kuehlen", "2", "Heizen", "Kuehlen")}
                                    {createSwitch("FREE", "3")}
                                    {createSwitch("Elektrisch heizen", "4")}
                                    {createSwitch("Zirkupumpe", "5")}
                                    {createSwitch("Solarpumpe", "6")}
                                </Grid>
                                <Grid item xs={4} container direction={"column"} spacing={2}>
                                    <Grid item container spacing={2} justifyContent={"center"}>
                                        {/*<Grid item xs={1}/>*/}
                                        <Grid item xs={8}><h2>Einstellungen</h2></Grid>
                                        {/*<Grid item xs={1}/>*/}
                                    </Grid>
                                    <Grid item container spacing={2} justifyContent={"center"}>
                                        <Grid item xs={4}>
                                            <LocalizationProvider dateAdapter={AdapterDateFns}>
                                                <MobileTimePicker
                                                    label="Wochentags Start"
                                                    value={value}
                                                    onChange={(newValue) => {
                                                        setValue(newValue);
                                                    }}
                                                    renderInput={(params) => <TextField {...params} />}
                                                />
                                            </LocalizationProvider>
                                        </Grid>

                                        <Grid item xs={4}>
                                            <LocalizationProvider dateAdapter={AdapterDateFns}>
                                                <MobileTimePicker
                                                    label="Wochentags Ende"
                                                    value={value}
                                                    onChange={(newValue) => {
                                                        setValue(newValue);
                                                    }}
                                                    renderInput={(params) => <TextField {...params} />}
                                                />
                                            </LocalizationProvider>
                                        </Grid>

                                    </Grid>

                                    <Grid item container spacing={2} justifyContent={"center"}>

                                        <Grid item xs={4}>
                                            <LocalizationProvider dateAdapter={AdapterDateFns}>
                                                <MobileTimePicker
                                                    label="Wochenends/Feiertags Start"
                                                    value={value}
                                                    onChange={(newValue) => {
                                                        setValue(newValue);
                                                    }}
                                                    renderInput={(params) => <TextField {...params} />}
                                                />

                                            </LocalizationProvider>
                                        </Grid>

                                        <Grid item xs={4}>
                                            <LocalizationProvider dateAdapter={AdapterDateFns}>
                                                <MobileTimePicker
                                                    label="Wochenends/Feiertags Ende"
                                                    value={value}
                                                    onChange={(newValue) => {
                                                        setValue(newValue);
                                                    }}
                                                    renderInput={(params) => <TextField {...params} />}
                                                />
                                            </LocalizationProvider>
                                        </Grid>

                                    </Grid>

                                    <Grid item container spacing={2} justifyContent={"center"}>
                                        <Grid item xs={1}/>

                                        <Grid item xs={6} container direction={"column"}>
                                            <Grid item>
                                                <p>Brauchwasser Max</p>
                                                <Slider
                                                    aria-label="Brauchwasser Max"
                                                    defaultValue={20}
                                                    getAriaValueText={valuetext}
                                                    step={10}
                                                    valueLabelDisplay="auto"
                                                    marks={marks}
                                                />
                                            </Grid>
                                            <Grid item>
                                                <p>Delta</p>
                                                <Slider
                                                    aria-label="Delta"
                                                    defaultValue={7}
                                                    max={10}
                                                    getAriaValueText={valuetext}
                                                    step={1}
                                                    valueLabelDisplay="auto"
                                                    marks={marks_delta}
                                                />
                                            </Grid>

                                        </Grid>

                                        <Grid item xs={1}/>

                                    </Grid>


                                </Grid>
                                <Grid item xs={1}/>
                            </Grid>
                        </Grid>
                    </Grid>

                </header>

            </div>
        </ThemeProvider>

    );
}


export default App;
