"""Trading Performance Report Importer"""

import pandas as pd
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

from .base import BaseImporter


class TradingPerformanceImporter(BaseImporter):
    """Import complete trading performance report from CSV"""
    
    REQUIRED_COLUMNS = [
        'entry_date', 'exit_date', 'symbol', 'entry_price', 'exit_price',
        'quantity', 'pnl', 'return_pct'
    ]
    
    OPTIONAL_COLUMNS = [
        'strategy', 'setup_type', 'notes', 'fees', 'duration_days'
    ]
    
    def validate(self) -> bool:
        """Validate CSV has required columns"""
        try:
            df = self.read_csv(nrows=1)  # Just check headers
            df_columns = [col.lower().strip() for col in df.columns]
            
            # Check for required columns (flexible matching)
            required_found = 0
            for req_col in self.REQUIRED_COLUMNS:
                for df_col in df_columns:
                    if req_col in df_col or df_col in req_col:
                        required_found += 1
                        break
            
            # Need at least most required columns
            return required_found >= len(self.REQUIRED_COLUMNS) * 0.7
        except Exception:
            return False
    
    def parse(self) -> Dict[str, Any]:
        """Parse trading performance CSV"""
        df = self.read_csv()
        
        # Normalize column names (lowercase, strip whitespace)
        df.columns = [col.lower().strip() for col in df.columns]
        
        # Map columns
        column_mapping = self._map_trading_columns(df.columns)
        df = df.rename(columns=column_mapping)
        
        # Clean data
        df = self._clean_data(df)
        
        # Calculate metrics
        metrics = self._calculate_metrics(df)
        
        # Extract top trades
        top_trades = self._extract_top_trades(df)
        
        return {
            'trades': df.to_dict('records'),
            'metrics': metrics,
            'top_trades': top_trades,
            'total_trades': len(df),
            'date_range': {
                'start': df['entry_date'].min() if 'entry_date' in df.columns else None,
                'end': df['exit_date'].max() if 'exit_date' in df.columns else None
            }
        }
    
    def _map_trading_columns(self, columns: List[str]) -> Dict[str, str]:
        """Map various column name formats to standard names"""
        mapping = {}
        
        # Common column name variations
        column_variations = {
            'entry_date': ['entry date', 'entry', 'open date', 'date', 'time', 'timestamp'],
            'exit_date': ['exit date', 'close date', 'closed', 'exit'],
            'symbol': ['symbol', 'ticker', 'pair', 'market', 'instrument'],
            'entry_price': ['entry price', 'entry', 'open price', 'open', 'buy price'],
            'exit_price': ['exit price', 'close price', 'close', 'sell price'],
            'quantity': ['quantity', 'size', 'amount', 'qty', 'volume'],
            'pnl': ['pnl', 'profit', 'profit_loss', 'profit/loss', 'realized pnl'],
            'return_pct': ['return', 'return %', 'return_pct', 'roi', 'return percent'],
            'strategy': ['strategy', 'type', 'trade type'],
            'setup_type': ['setup', 'setup type', 'pattern', 'signal'],
            'fees': ['fees', 'commission', 'fee'],
            'notes': ['notes', 'note', 'comment', 'description']
        }
        
        columns_lower = [col.lower() for col in columns]
        
        for standard_name, variations in column_variations.items():
            for col in columns:
                col_lower = col.lower()
                if col_lower == standard_name or any(var in col_lower for var in variations):
                    mapping[col] = standard_name
                    break
        
        return mapping
    
    def _clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and normalize data"""
        # Convert dates
        date_columns = ['entry_date', 'exit_date']
        for col in date_columns:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')
        
        # Convert numeric columns
        numeric_columns = ['entry_price', 'exit_price', 'quantity', 'pnl', 'return_pct', 'fees']
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Calculate return_pct if not present but have entry/exit prices
        if 'return_pct' not in df.columns and 'entry_price' in df.columns and 'exit_price' in df.columns:
            df['return_pct'] = ((df['exit_price'] - df['entry_price']) / df['entry_price']) * 100
        
        # Calculate duration if dates available
        if 'entry_date' in df.columns and 'exit_date' in df.columns:
            df['duration_days'] = (df['exit_date'] - df['entry_date']).dt.days
        
        # Remove rows with missing critical data
        critical_cols = ['entry_date', 'exit_date', 'symbol', 'pnl']
        df = df.dropna(subset=[col for col in critical_cols if col in df.columns], how='all')
        
        return df
    
    def _calculate_metrics(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Calculate performance metrics"""
        if df.empty:
            return {}
        
        metrics = {}
        
        # Basic metrics
        if 'pnl' in df.columns:
            metrics['total_pnl'] = float(df['pnl'].sum())
            metrics['avg_pnl'] = float(df['pnl'].mean())
            metrics['win_rate'] = float((df['pnl'] > 0).sum() / len(df) * 100) if len(df) > 0 else 0
            
            winning_trades = df[df['pnl'] > 0]
            losing_trades = df[df['pnl'] < 0]
            
            metrics['avg_win'] = float(winning_trades['pnl'].mean()) if len(winning_trades) > 0 else 0
            metrics['avg_loss'] = float(losing_trades['pnl'].mean()) if len(losing_trades) > 0 else 0
            metrics['profit_factor'] = abs(metrics['avg_win'] / metrics['avg_loss']) if metrics['avg_loss'] != 0 else 0
        
        # Return metrics
        if 'return_pct' in df.columns:
            metrics['total_return_pct'] = float(df['return_pct'].sum())
            metrics['avg_return_pct'] = float(df['return_pct'].mean())
        
        # Drawdown calculation (simplified)
        if 'pnl' in df.columns:
            cumulative = df['pnl'].cumsum()
            running_max = cumulative.expanding().max()
            drawdown = cumulative - running_max
            metrics['max_drawdown'] = float(drawdown.min())
        
        # Sharpe ratio (simplified, assuming daily returns)
        if 'return_pct' in df.columns and len(df) > 1:
            returns = df['return_pct']
            if returns.std() > 0:
                metrics['sharpe_ratio'] = float(returns.mean() / returns.std() * (252 ** 0.5))  # Annualized
            else:
                metrics['sharpe_ratio'] = 0.0
        
        # Strategy distribution
        if 'strategy' in df.columns:
            strategy_counts = df['strategy'].value_counts().to_dict()
            metrics['strategy_distribution'] = {k: int(v) for k, v in strategy_counts.items()}
        
        return metrics
    
    def _extract_top_trades(self, df: pd.DataFrame, top_n: int = 10) -> List[Dict[str, Any]]:
        """Extract top N trades by PnL"""
        if df.empty or 'pnl' not in df.columns:
            return []
        
        top_trades_df = df.nlargest(top_n, 'pnl')
        return top_trades_df.to_dict('records')

