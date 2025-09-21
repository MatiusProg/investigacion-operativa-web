# -*- coding: utf-8 -*-
# type: ignore
import plotly.graph_objects as go
import plotly.io as pio
import numpy as np
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.graphic_method import LinearProgrammingProblem

class InteractiveLinearProgramming(LinearProgrammingProblem):
    def create_interactive_plot(self, feasible_points, optimal_point):
        """Crea gráfico interactivo con ejes destacados"""
        try:
            fig = go.Figure()
            
            if not feasible_points:
                return None
                
            # Calcular límites 
            all_x = [p[0] for p in feasible_points]
            all_y = [p[1] for p in feasible_points]
            max_x = max(all_x) * 1.5
            max_y = max(all_y) * 1.5
            
            # Colores - EJES MÁS DESTACADOS
            colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#F9A602', '#9F7AEA', '#FF8066']
            
            # 0. PRIMERO: GRAFICAR EJES COORDENADOS (¡MÁS DESTACADOS!)
            fig.add_trace(go.Scatter(
                x=[-max_x*0.1, max_x*1.1], y=[0, 0],
                mode='lines',
                line=dict(color='black', width=3),
                name='Eje X',
                hoverinfo='none',
                showlegend=True
            ))
            
            fig.add_trace(go.Scatter(
                x=[0, 0], y=[-max_y*0.1, max_y*1.1],
                mode='lines',
                line=dict(color='black', width=3),
                name='Eje Y',
                hoverinfo='none',
                showlegend=True
            ))
            
            # Añadir flechas a los ejes
            fig.add_annotation(
                x=max_x*1.1, y=0,
                ax=20, ay=0,
                xref='x', yref='y',
                axref='x', ayref='y',
                showarrow=True,
                arrowhead=2,
                arrowsize=1.5,
                arrowwidth=2,
                arrowcolor='black'
            )
            
            fig.add_annotation(
                x=0, y=max_y*1.1,
                ax=0, ay=20,
                xref='x', yref='y',
                axref='x', ayref='y',
                showarrow=True,
                arrowhead=2,
                arrowsize=1.5,
                arrowwidth=2,
                arrowcolor='black'
            )
            
            # 1. LUEGO: REGIÓN FACTIBLE
            if len(feasible_points) >= 3:
                from scipy.spatial import ConvexHull
                points = np.array(feasible_points)
                hull = ConvexHull(points)
                
                poly_x = points[hull.vertices, 0].tolist() + [points[hull.vertices[0], 0]]
                poly_y = points[hull.vertices, 1].tolist() + [points[hull.vertices[0], 1]]
                
                fig.add_trace(go.Scatter(
                    x=poly_x, y=poly_y,
                    fill='toself',
                    fillcolor='rgba(100, 250, 100, 0.8)',  # ← Más transparente
                    line=dict(color='green', width=2, dash='solid'),
                    name='Región Factible',
                    hoverinfo='none',
                    showlegend=True
                ))
            
            # 2. RESTRICCIONES (estilo más sutil)
            for i, constraint in enumerate(self.constraints):
                try:
                    coefficients, right_side, inequality = self.parse_constraint(constraint)
                    a, b = coefficients
                    
                    color = colors[i % len(colors)]
                    
                    # Puntos extremos extendidos
                    x_extreme = [-max_x * 2, max_x * 2]
                    y_extreme = [-max_y * 2, max_y * 2]
                    
                    if abs(b) > 1e-10:  # Recta normal
                        y1 = (right_side - a * x_extreme[0]) / b
                        y2 = (right_side - a * x_extreme[1]) / b
                        fig.add_trace(go.Scatter(
                            x=x_extreme, y=[y1, y2],
                            mode='lines',
                            name=f'R{i+1}: {constraint}',
                            line=dict(color=color, width=2, dash='solid'),  # ← LÍNEA SÓLIDA
                            hoverinfo='name',
                            showlegend=True,
                            opacity=0.8  # ← Más transparente
                        ))
                        
                    elif abs(a) > 1e-10:  # Línea vertical
                        x_val = right_side / a
                        fig.add_trace(go.Scatter(
                            x=[x_val, x_val], y=y_extreme,
                            mode='lines',
                            name=f'R{i+1}: {constraint}',
                            line=dict(color=color, width=2, dash='solid'),  # ← LÍNEA SÓLIDA
                            hoverinfo='name',
                            showlegend=True,
                            opacity=0.8  # ← Más transparente
                        ))
                        
                except Exception as e:
                    print(f"⚠️ Error graficando restricción {constraint}: {e}")
            
            # 3. CUADRANTE NO NEGATIVIDAD
            fig.add_trace(go.Scatter(
                x=[0, max_x*1.1, max_x*1.1, 0, 0],
                y=[0, 0, max_y*1.1, max_y*1.1, 0],
                fill='toself',
                fillcolor='rgba(200, 200, 200, 0)',  # ← Sombreado muy suave
                line=dict(width=0),
                name='x ≥ 0, y ≥ 0',
                hoverinfo='none',
                showlegend=True
            ))
            
            # 4. VÉRTICES FACTIBLES
            fig.add_trace(go.Scatter(
                x=[p[0] for p in feasible_points],
                y=[p[1] for p in feasible_points],
                mode='markers',
                marker=dict(
                    color='pink', 
                    size=8, 
                    symbol='circle',
                    line=dict(width=1.5, color='darkblue')
                ),
                name='Vértices Factibles',
                hoverinfo='text',
                hovertext=[f'Vértice: ({p[0]:.2f}, {p[1]:.2f})' for p in feasible_points],
                showlegend=True
            ))
            
            # 5. PUNTO ÓPTIMO (¡MÁS DESTACADO!)
            if optimal_point:
                fig.add_trace(go.Scatter(
                    x=[optimal_point[0]], y=[optimal_point[1]],
                    mode='markers+text',
                    marker=dict(
                        size=7,  # ← Más grande
                        color='gold',
                        line=dict(width=1, color='gold')  # ← Borde rojo
                    ),
                    text=['ÓPTIMO'],
                    textfont=dict(size=16, color='brown', weight='bold'),  # ← Texto rojo
                    textposition='top center',
                    name=f'Óptimo: ({optimal_point[0]:.2f}, {optimal_point[1]:.2f})',
                    hoverinfo='text',
                    hovertext=f'Óptimo: ({optimal_point[0]:.2f}, {optimal_point[1]:.2f})<br>Valor: {self.optimal_value:.2f}',
                    showlegend=True
                ))
            
            # CONFIGURACIÓN FINAL CON EJES DESTACADOS
            fig.update_layout(
                title=dict(
                    text='<b>SOLUCIÓN MÉTODO GRÁFICO</b><br><sub>Programación Lineal</sub>',
                    x=0.5,
                    font=dict(size=22, family='Arial', color='#2c3e50')
                ),
                xaxis=dict(
                    title=dict(text='<b>VARIABLE X</b>', font=dict(size=16, color='black')),
                    range=[-max_x*0.1, max_x*1.1],
                    gridcolor='rgba(200, 200, 200, 0.8)',  # ← Grid MUY suave
                    zeroline=False,
                    showgrid=True,
                    tickfont=dict(size=12, color='black'),
                    showline=True,  # ← Mostrar línea del eje
                    linecolor='black',  # ← Color de línea del eje
                    linewidth=3  # ← Grosor de línea del eje
                ),
                yaxis=dict(
                    title=dict(text='<b>VARIABLE Y</b>', font=dict(size=16, color='black')),
                    range=[-max_y*0.1, max_y*1.1],
                    gridcolor='rgba(200, 200, 200, 0.8)',  # ← Grid MUY suave
                    zeroline=True,
                    showgrid=True,
                    tickfont=dict(size=12, color='black'),
                    showline=True,  # ← Mostrar línea del eje
                    linecolor='black',  # ← Color de línea del eje
                    linewidth=3  # ← Grosor de línea del eje
                ),
                legend=dict(
                    x=1.05,
                    y=1,
                    xanchor='left',
                    yanchor='top',
                    bgcolor='rgba(255, 255, 255, 0.9)',
                    bordercolor='gray',
                    borderwidth=1,
                    font=dict(size=11)
                ),
                hovermode='closest',
                width=1000,
                height=700,
                plot_bgcolor='white',
                paper_bgcolor='white',
                margin=dict(l=80, r=80, t=100, b=80),
                font=dict(family='Arial', size=12, color='#2c3e50')
            )
            
            # HABILITAR INTERACTIVIDAD
            fig.update_xaxes(fixedrange=False, showspikes=True)
            fig.update_yaxes(fixedrange=False, showspikes=True)
            
            return pio.to_html(fig, include_plotlyjs='cdn', full_html=False)
            
        except Exception as e:
            print(f"Error creando gráfico interactivo: {e}")
            import traceback
            traceback.print_exc()
            return None

    def solve_interactive(self):
        """Resuelve y retorna gráfico interactivo"""
        result = self.solve()
        
        if "error" in result:
            return result
        
        # Guardar optimal_value para el hover
        self.optimal_value = result["optimal_value"]
        
        interactive_html = self.create_interactive_plot(
            result["feasible_vertices"], 
            result["optimal_point"]
        )
        
        if interactive_html:
            result["interactive_plot"] = interactive_html
        else:
            result["interactive_plot"] = None
        
        return result